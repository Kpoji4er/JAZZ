[CmdletBinding()]
param(
    [string]$SuiteRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path,
    [switch]$RequireCurrentCommonLibDependency,
    [switch]$IncludeMapsContent,
    [ValidateRange(1, 168)]
    [int]$CommonLibSnapshotTtlHours = 24,
    [switch]$RefreshCommonLibSnapshot,
    [switch]$DetailedStatus
)

$ErrorActionPreference = 'Stop'
$main = Resolve-Path $SuiteRoot
$parent = Split-Path $main -Parent
$specs = @(
    @{ Name = 'jazz'; Candidates = @($main.Path) },
    @{ Name = 'jazz-assets'; Candidates = @((Join-Path $parent 'jazz_assets'), (Join-Path $parent 'jazz-assets')) },
    @{ Name = 'jazz-maps'; Candidates = @((Join-Path $parent 'jazz-maps')) },
    @{ Name = 'jazz-units'; Candidates = @((Join-Path $parent 'jazz-units')) }
)

$repos = @()
foreach ($spec in $specs) {
    $path = $spec.Candidates | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -First 1
    if (-not $path) {
        Write-Warning "Не найден соседний репозиторий: $($spec.Name)"
        continue
    }
    $repos += [pscustomobject]@{ Name = $spec.Name; Path = (Resolve-Path $path).Path }
}

Write-Host "Комплект JAZZ: $($main.Path)"
foreach ($repo in $repos) {
    Write-Host "`n[$($repo.Name)] $($repo.Path)"
    if (Test-Path -LiteralPath (Join-Path $repo.Path '.git')) {
        if ($repo.Name -eq 'jazz-maps' -and -not $IncludeMapsContent) {
            $statusLines = @(git -C $repo.Path status --short -- . ':(exclude)Maps/**')
        } else {
            $statusLines = @(git -C $repo.Path status --short)
        }
        if ($LASTEXITCODE -ne 0) {
            Write-Warning 'Не удалось прочитать Git status.'
        } else {
            Write-Host ("Git status: {0} change(s){1}" -f $statusLines.Count, $(if ($repo.Name -eq 'jazz-maps' -and -not $IncludeMapsContent) { ' outside Maps/' } else { '' }))
            if ($DetailedStatus) { $statusLines | Write-Output }
        }
    } else {
        Write-Warning 'Каталог не является рабочим деревом Git.'
    }

    $codeRoot = Join-Path $repo.Path 'Code'
    if (Test-Path -LiteralPath $codeRoot) {
        $files = @(Get-ChildItem -LiteralPath $codeRoot -Recurse -File -Filter '*.lua')
        $special = @($files | Where-Object { $_.Name -match '^(FX_|CodeSounds)' }).Count
        Write-Host ("Lua-файлы в Code/: всего {0}; FX/audio helpers — {1}" -f $files.Count, $special)
    }
}

$commonLibRemote = 'https://gitlab.com/injto4ka/ja3_commonlib.git'
$commonLibMetadata = 'https://gitlab.com/injto4ka/ja3_commonlib/-/raw/main/metadata.lua'
$commonLibVerified = $false
$commonLibDependencyIssues = @()
$commonLibCachePath = Join-Path ([IO.Path]::GetTempPath()) 'jazz-commonlib-main-snapshot.json'
try {
    $snapshot = $null
    $snapshotSource = 'upstream'
    if (-not $RefreshCommonLibSnapshot -and (Test-Path -LiteralPath $commonLibCachePath -PathType Leaf)) {
        try {
            $cached = Get-Content -LiteralPath $commonLibCachePath -Raw | ConvertFrom-Json
            $verifiedAt = [datetime]::Parse($cached.verified_at_utc).ToUniversalTime()
            $age = [datetime]::UtcNow - $verifiedAt
            if ($age.TotalHours -le $CommonLibSnapshotTtlHours -and
                [string]$cached.commit -match '^[0-9a-f]{40}$' -and
                [int]$cached.major -ge 0 -and [int]$cached.minor -ge 0 -and [int]$cached.build -ge 0) {
                $snapshot = $cached
                $snapshotSource = "cache ($([math]::Round($age.TotalHours, 1))h old)"
            }
        } catch {
            $snapshot = $null
        }
    }

    if (-not $snapshot) {
        $remoteLines = @(& git ls-remote $commonLibRemote refs/heads/main 2>&1)
        $remoteExitCode = $LASTEXITCODE
        $remoteLine = $remoteLines | Select-Object -First 1
        if ($remoteExitCode -ne 0 -or -not $remoteLine) { throw "Не удалось определить CommonLib main (код git: $remoteExitCode)." }
        $remoteCommit = ([string]$remoteLine -split '\s+')[0]
        if ($remoteCommit -notmatch '^[0-9a-f]{40}$') { throw "Неожиданное значение commit CommonLib: $remoteCommit" }
        $metadata = (Invoke-WebRequest -UseBasicParsing -Uri $commonLibMetadata).Content
        $major = [regex]::Match($metadata, "'version_major',\s*(\d+)").Groups[1].Value
        $minor = [regex]::Match($metadata, "'version_minor',\s*(\d+)").Groups[1].Value
        $build = [regex]::Match($metadata, "'version',\s*(\d+)").Groups[1].Value
        if (-not $major -or -not $minor -or -not $build) { throw 'Не удалось прочитать версию CommonLib из upstream metadata.lua.' }
        $snapshot = [pscustomobject]@{
            schema = 1
            commit = $remoteCommit
            major = [int]$major
            minor = [int]$minor
            build = [int]$build
            verified_at_utc = [datetime]::UtcNow.ToString('o')
        }
        [IO.File]::WriteAllText($commonLibCachePath, ($snapshot | ConvertTo-Json -Depth 3), [Text.UTF8Encoding]::new($false))
    }

    $remoteCommit = [string]$snapshot.commit
    $major = [string]$snapshot.major
    $minor = [string]$snapshot.minor
    $build = [string]$snapshot.build
    Write-Host "`nCommonLib snapshot ($snapshotSource): $major.$minor, build $build, commit $remoteCommit"

    foreach ($repo in $repos) {
        $repoMetadataPath = Join-Path $repo.Path 'metadata.lua'
        if (-not (Test-Path -LiteralPath $repoMetadataPath -PathType Leaf)) { continue }
        $repoMetadata = [IO.File]::ReadAllText($repoMetadataPath)
        $dependencyBlocks = [regex]::Matches($repoMetadata, "(?s)PlaceObj\('ModDependency',\s*\{.*?\}\)")
        $commonLibBlock = $dependencyBlocks | Where-Object { $_.Value -match '''id'',\s*"JA3_CommonLib"' } | Select-Object -First 1
        if (-not $commonLibBlock) { continue }
        $declaredMajor = [regex]::Match($commonLibBlock.Value, '''version_major'',\s*(\d+)').Groups[1].Value
        $declaredMinor = [regex]::Match($commonLibBlock.Value, '''version_minor'',\s*(\d+)').Groups[1].Value
        if (-not $declaredMajor) { $declaredMajor = '0' }
        if (-not $declaredMinor) { $declaredMinor = '0' }
        if ($declaredMajor -ne $major -or $declaredMinor -ne $minor) {
            $commonLibDependencyIssues += "[$($repo.Name)] объявлена JA3_CommonLib $declaredMajor.$declaredMinor; актуальная версия — $major.$minor."
        } else {
            Write-Host "[$($repo.Name)] dependency JA3_CommonLib актуальна: $declaredMajor.$declaredMinor"
        }
    }
    if ($commonLibDependencyIssues) {
        Write-Warning 'Найдены устаревшие объявления зависимости CommonLib:'
        $commonLibDependencyIssues | ForEach-Object { Write-Warning $_ }
    }
    $commonLibVerified = $true
} catch {
    Write-Warning "Последняя версия CommonLib не подтверждена: $($_.Exception.Message)"
}

$markdown = foreach ($repo in $repos) {
    if (Test-Path -LiteralPath (Join-Path $repo.Path '.git')) {
        $pathspec = @('*.md')
        if ($repo.Name -eq 'jazz-maps' -and -not $IncludeMapsContent) {
            $pathspec += ':(exclude)Maps/**'
        }
        $relativePaths = @(& git -C $repo.Path ls-files --cached --others --exclude-standard -- $pathspec)
        if ($LASTEXITCODE -ne 0) {
            throw "Не удалось получить Markdown inventory: $($repo.Name)"
        }
        foreach ($relativePath in $relativePaths) {
            $fullPath = Join-Path $repo.Path $relativePath
            if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
                Get-Item -LiteralPath $fullPath
            }
        }
    } else {
        Get-ChildItem -LiteralPath $repo.Path -File -Filter '*.md' -ErrorAction SilentlyContinue
    }
}

$leaks = foreach ($file in $markdown) {
    Select-String -LiteralPath $file.FullName -Pattern '(?i)\b[A-Z]:[\\/]' -AllMatches -ErrorAction SilentlyContinue
}
if ($leaks) {
    Write-Warning 'В Markdown найдены абсолютные пути Windows:'
    $leaks | ForEach-Object { Write-Host ("{0}:{1}" -f $_.Path, $_.LineNumber) }
} else {
    Write-Host "`nАбсолютных путей Windows в Markdown не найдено."
}

if ($repos.Count -ne 4 -or $leaks -or -not $commonLibVerified) { exit 1 }
if ($RequireCurrentCommonLibDependency -and $commonLibDependencyIssues) { exit 2 }
exit 0
