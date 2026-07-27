[CmdletBinding()]
param(
    [string]$SuiteRoot,
    [ValidateSet('jazz', 'jazz_assets', 'jazz-maps', 'jazz-units')]
    [string[]]$Package,
    [switch]$Strict,
    [switch]$DetailedWarnings,
    [switch]$IncludeMapsContent
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:issues = New-Object 'System.Collections.Generic.List[object]'
$script:fatal = $false

function Add-Issue {
    param(
        [string]$Level,
        [string]$Repo,
        [string]$Path,
        [string]$Message
    )

    $script:issues.Add([pscustomobject]@{
        Level = $Level
        Repo = $Repo
        Path = $Path
        Message = $Message
    }) | Out-Null
}

function Normalize-RelativePath {
    param([string]$Path)
    if ([string]::IsNullOrWhiteSpace($Path)) { return '' }
    return $Path.Replace('\', '/').TrimStart('./')
}

function Read-Utf8Text {
    param([string]$Path)
    return [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
}

function Get-MetadataList {
    param(
        [string]$Text,
        [string]$FieldName
    )

    $pattern = "(?ms)^(?<indent>[ `t]*)'" + [regex]::Escape($FieldName) + "',\s*\{\s*\r?\n(?<body>.*?)^\k<indent>\},\s*$"
    $match = [regex]::Match($Text, $pattern)
    if (-not $match.Success) {
        return [pscustomobject]@{ Found = $false; Values = @() }
    }

    $values = New-Object 'System.Collections.Generic.List[string]'
    foreach ($stringMatch in [regex]::Matches($match.Groups['body'].Value, '"(?<value>(?:\\.|[^"\\])*)"')) {
        $values.Add($stringMatch.Groups['value'].Value) | Out-Null
    }
    return [pscustomobject]@{ Found = $true; Values = @($values) }
}

function Get-StringProperty {
    param(
        [string]$Body,
        [string]$Name
    )

    $escaped = [regex]::Escape($Name)
    $quotedPattern = '(?m)^[ \t]*''{0}'',\s*"(?<value>[^"\r\n]*)"' -f $escaped
    $barePattern = '(?m)^[ \t]*{0}\s*=\s*"(?<value>[^"\r\n]*)"' -f $escaped
    foreach ($pattern in @($quotedPattern, $barePattern)) {
        $match = [regex]::Match($Body, $pattern)
        if ($match.Success) { return $match.Groups['value'].Value }
    }
    return $null
}

function Get-ModItemRecords {
    param([string]$Text)

    $pattern = "(?ms)^(?<indent>[ `t]*)PlaceObj\('(?<class>ModItem[^']*)',\s*\{\s*\r?\n(?<body>.*?)^\k<indent>\}(?:\)|,\s*\{)"
    foreach ($match in [regex]::Matches($Text, $pattern)) {
        $body = $match.Groups['body'].Value
        $id = Get-StringProperty -Body $body -Name 'Id'
        if ([string]::IsNullOrEmpty($id)) { $id = Get-StringProperty -Body $body -Name 'id' }
        $name = Get-StringProperty -Body $body -Name 'name'
        $entityName = Get-StringProperty -Body $body -Name 'entity_name'
        $codeFileName = Get-StringProperty -Body $body -Name 'CodeFileName'

        [pscustomobject]@{
            Class = $match.Groups['class'].Value
            Id = $id
            Name = $name
            EntityName = $entityName
            CodeFileName = $codeFileName
            Offset = $match.Index
        }
    }
}

function Get-SafePresetId {
    param([string]$Id)
    if ($null -eq $Id) { return '' }
    return [regex]::Replace($Id, '[\p{Cc}\p{Cf}\p{P}\p{Z}\p{S}]', '_')
}

if ([string]::IsNullOrWhiteSpace($SuiteRoot)) {
    $SuiteRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\..'))
} else {
    $SuiteRoot = [IO.Path]::GetFullPath($SuiteRoot)
}

$suiteParent = Split-Path -Parent $SuiteRoot

function Resolve-SuitePackageRoot {
    param([string[]] $Names)
    foreach ($name in $Names) {
        $candidate = Join-Path $suiteParent $name
        if (Test-Path -LiteralPath $candidate -PathType Container) {
            return [IO.Path]::GetFullPath($candidate)
        }
    }
    # Fallback to the first candidate so missing-package diagnostics keep a path.
    return [IO.Path]::GetFullPath((Join-Path $suiteParent $Names[0]))
}

$packageRoots = [ordered]@{
    'jazz' = $SuiteRoot
    'jazz_assets' = Resolve-SuitePackageRoot -Names @('jazz_assets', 'jazz-assets', 'Jazz Assets', 'jazz assets')
    'jazz-maps' = Resolve-SuitePackageRoot -Names @('jazz-maps', 'JAZZ Maps', 'jazz maps')
    'jazz-units' = Resolve-SuitePackageRoot -Names @('jazz-units', 'JAZZ Units', 'jazz units')
}

$selectedNames = if ($Package -and $Package.Count -gt 0) { @($Package) } else { @($packageRoots.Keys) }

Write-Output 'JAZZ generated-data sync audit (read-only)'
Write-Output ('Packages: ' + ($selectedNames -join ', '))

foreach ($repoName in $selectedNames) {
    $repoRoot = $packageRoots[$repoName]
    if (-not (Test-Path -LiteralPath $repoRoot -PathType Container)) {
        Add-Issue -Level 'FATAL' -Repo $repoName -Path '.' -Message 'Каталог пакета не найден.'
        $script:fatal = $true
        continue
    }

    $metadataPath = Join-Path $repoRoot 'metadata.lua'
    $itemsPath = Join-Path $repoRoot 'items.lua'
    foreach ($core in @($metadataPath, $itemsPath)) {
        if (-not (Test-Path -LiteralPath $core -PathType Leaf)) {
            Add-Issue -Level 'FATAL' -Repo $repoName -Path ([IO.Path]::GetFileName($core)) -Message 'Обязательный generated-data файл не найден.'
            $script:fatal = $true
        }
    }
    if (-not (Test-Path -LiteralPath $metadataPath -PathType Leaf) -or -not (Test-Path -LiteralPath $itemsPath -PathType Leaf)) {
        continue
    }

    try {
        $metadataText = Read-Utf8Text $metadataPath
        $itemsText = Read-Utf8Text $itemsPath
        $codeResult = Get-MetadataList -Text $metadataText -FieldName 'code'
        $entityResult = Get-MetadataList -Text $metadataText -FieldName 'entities'
        if (-not $codeResult.Found) {
            Add-Issue -Level 'FATAL' -Repo $repoName -Path 'metadata.lua' -Message 'Не удалось разобрать массив code.'
            $script:fatal = $true
            continue
        }
        $codePaths = @($codeResult.Values | ForEach-Object { Normalize-RelativePath $_ })
        $metadataEntities = if ($entityResult.Found) { @($entityResult.Values) } else { @() }
        $records = @(Get-ModItemRecords -Text $itemsText)
    } catch {
        Add-Issue -Level 'FATAL' -Repo $repoName -Path '.' -Message ('Ошибка разбора generated data: ' + $_.Exception.Message)
        $script:fatal = $true
        continue
    }

    $codeSet = @{}
    foreach ($codePath in $codePaths) {
        if ($codeSet.ContainsKey($codePath)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path 'metadata.lua' -Message ("Путь code продублирован: {0}" -f $codePath)
        } else {
            $codeSet[$codePath] = $true
        }
        $diskPath = Join-Path $repoRoot ($codePath.Replace('/', '\'))
        if (-not (Test-Path -LiteralPath $diskPath -PathType Leaf)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path $codePath -Message 'Путь из metadata.code не существует.'
        }
    }

    $itemKeys = @{}
    $entityItems = @{}
    foreach ($record in $records) {
        if (-not [string]::IsNullOrEmpty($record.Id)) {
            $itemKeys[($record.Class + '|' + $record.Id)] = $true
        }
        if (-not [string]::IsNullOrEmpty($record.EntityName)) {
            $entityItems[$record.EntityName] = $record
        }
    }

    $generated = New-Object 'System.Collections.Generic.List[object]'
    $classFolders = @{}
    $excludedTopLevel = @('.git', '.agents', '.codex', '.openai', 'codex_worktrees', 'docs', 'Code', 'Entities')
    if ($repoName -eq 'jazz-maps' -and -not $IncludeMapsContent) {
        $excludedTopLevel += 'Maps'
    }
    $scanRoots = Get-ChildItem -LiteralPath $repoRoot -Directory -Force | Where-Object {
        $_.Name -notin $excludedTopLevel
    }
    $luaFiles = @(
        Get-ChildItem -LiteralPath $repoRoot -File -Filter '*.lua'
        foreach ($scanRoot in $scanRoots) {
            Get-ChildItem -LiteralPath $scanRoot.FullName -Recurse -File -Filter '*.lua'
        }
    ) | Where-Object {
        $_.Name -notin @('items.lua', 'metadata.lua') -and
        $_.FullName -notmatch '\\(?:\.git|\.agents|\.codex|\.openai|codex_worktrees|docs|Code|Entities)\\'
    }

    foreach ($file in $luaFiles) {
        $text = Read-Utf8Text $file.FullName
        $classMatch = [regex]::Match($text, '__generated_by_class\s*=\s*"(?<class>[^"]+)"')
        if (-not $classMatch.Success) { continue }
        $idMatch = [regex]::Match($text, 'UndefineClass\(["''](?<id>[^"'']+)["'']\)')
        if (-not $idMatch.Success) {
            $relative = Normalize-RelativePath ($file.FullName.Substring($repoRoot.Length).TrimStart('\', '/'))
            Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Generated marker найден, но UndefineClass ID не разобран.'
            continue
        }

        $relative = Normalize-RelativePath ($file.FullName.Substring($repoRoot.Length).TrimStart('\', '/'))
        $entry = [pscustomobject]@{
            Class = $classMatch.Groups['class'].Value
            Id = $idMatch.Groups['id'].Value
            RelativePath = $relative
            FullName = $file.FullName
        }
        $generated.Add($entry) | Out-Null

        $folder = Normalize-RelativePath (Split-Path -Parent $relative)
        if (-not $classFolders.ContainsKey($entry.Class)) {
            $classFolders[$entry.Class] = New-Object 'System.Collections.Generic.List[string]'
        }
        if (-not $classFolders[$entry.Class].Contains($folder)) {
            $classFolders[$entry.Class].Add($folder) | Out-Null
        }

        $hasCodePath = $codeSet.ContainsKey($relative)
        $hasModItem = $itemKeys.ContainsKey($entry.Class + '|' + $entry.Id)
        if (-not $hasCodePath -and -not $hasModItem) {
            Add-Issue -Level 'WARNING' -Repo $repoName -Path $relative -Message ("Generated companion находится вне активного items/metadata graph; классифицировать как intentional dormant или orphan: {0} / {1}." -f $entry.Class, $entry.Id)
        } else {
            if (-not $hasCodePath) {
                Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Активный generated companion отсутствует в metadata.code.'
            }
            if (-not $hasModItem) {
                Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message ("Активный generated companion не имеет ModItem в items.lua: {0} / {1}." -f $entry.Class, $entry.Id)
            }
        }
    }

    foreach ($record in $records) {
        if ([string]::IsNullOrEmpty($record.Id) -or -not $classFolders.ContainsKey($record.Class)) { continue }
        $folders = $classFolders[$record.Class]
        if ($folders.Count -ne 1) { continue }
        $expectedRelative = Normalize-RelativePath ($folders[0] + '/' + (Get-SafePresetId $record.Id) + '.lua')
        $expectedFull = Join-Path $repoRoot ($expectedRelative.Replace('/', '\'))
        if (-not (Test-Path -LiteralPath $expectedFull -PathType Leaf)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path $expectedRelative -Message ("ModItem существует, но ожидаемый generated companion не найден: {0} / {1}." -f $record.Class, $record.Id)
        }
    }

    $entitySet = @{}
    foreach ($entity in $metadataEntities) { $entitySet[$entity] = $true }
    $entityDir = Join-Path $repoRoot 'Entities'
    $entityFiles = @()
    if (Test-Path -LiteralPath $entityDir -PathType Container) {
        $entityFiles = @(Get-ChildItem -LiteralPath $entityDir -File -Filter '*.lua')
    }
    $entityFileByKey = @{}

    foreach ($file in $entityFiles) {
        $relative = Normalize-RelativePath ($file.FullName.Substring($repoRoot.Length).TrimStart('\', '/'))
        $text = Read-Utf8Text $file.FullName
        $keyMatch = [regex]::Match($text, 'EntityData\[["''](?<id>[^"'']+)["'']\]\s*=')
        if (-not $keyMatch.Success) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Не удалось разобрать ключ EntityData.'
            continue
        }
        $entityKey = $keyMatch.Groups['id'].Value
        $entityFileByKey[$entityKey] = $relative
        $hasItem = $entityItems.ContainsKey($entityKey)
        $hasMetadataEntity = $entitySet.ContainsKey($entityKey)
        $hasCodePath = $codeSet.ContainsKey($relative)
        if (-not $hasItem -and -not $hasMetadataEntity -and -not $hasCodePath) {
            Add-Issue -Level 'WARNING' -Repo $repoName -Path $relative -Message 'Entity-файл вне активного графа items/metadata; проверить, является ли он orphan или намеренно dormant.'
        } else {
            if (-not $hasItem) {
                Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Активный Entity companion не имеет ModItemEntity в items.lua.'
            }
            if (-not $hasMetadataEntity) {
                Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Активный Entity companion отсутствует в metadata.entities.'
            }
            if (-not $hasCodePath) {
                Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'Активный Entity companion отсутствует в metadata.code.'
            }
        }
    }

    foreach ($entityName in $entityItems.Keys) {
        $relative = Normalize-RelativePath ('Entities/' + $entityName + '.lua')
        if (-not $entitySet.ContainsKey($entityName)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path 'metadata.lua' -Message ("ModItemEntity отсутствует в metadata.entities: {0}." -f $entityName)
        }
        if (-not $codeSet.ContainsKey($relative)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path 'metadata.lua' -Message ("ModItemEntity companion отсутствует в metadata.code: {0}." -f $relative)
        }
        if (-not $entityFileByKey.ContainsKey($entityName)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path $relative -Message 'ModItemEntity существует, но companion не найден или имеет другой EntityData key.'
        }
    }

    foreach ($entityName in $entitySet.Keys) {
        if (-not $entityItems.ContainsKey($entityName)) {
            Add-Issue -Level 'ERROR' -Repo $repoName -Path 'metadata.lua' -Message ("metadata.entities не имеет ModItemEntity в items.lua: {0}." -f $entityName)
        }
    }

    $itemsTime = (Get-Item -LiteralPath $itemsPath).LastWriteTimeUtc
    $metadataTime = (Get-Item -LiteralPath $metadataPath).LastWriteTimeUtc
    if (($metadataTime - $itemsTime).TotalSeconds -gt 2) {
        Add-Issue -Level 'WARNING' -Repo $repoName -Path 'metadata.lua' -Message 'metadata.lua новее items.lua; возможна незавершённая транзакция или внешняя правка.'
    }
    $newerGenerated = @()
    foreach ($entry in $generated) {
        $companionTime = (Get-Item -LiteralPath $entry.FullName).LastWriteTimeUtc
        if (($companionTime - $itemsTime).TotalSeconds -gt 2) {
            $newerGenerated += $entry.RelativePath
        }
    }
    if ($newerGenerated.Count -gt 0) {
        $sample = ($newerGenerated | Select-Object -First 5) -join ', '
        Add-Issue -Level 'WARNING' -Repo $repoName -Path 'items.lua' -Message ("{0} generated companion новее items.lua; проверить перенос в ModItem. Примеры: {1}" -f $newerGenerated.Count, $sample)
    }

    $newerEntities = @()
    foreach ($file in $entityFiles) {
        if (($file.LastWriteTimeUtc - $itemsTime).TotalSeconds -gt 2) {
            $newerEntities += Normalize-RelativePath ($file.FullName.Substring($repoRoot.Length).TrimStart('\', '/'))
        }
    }
    if ($newerEntities.Count -gt 0) {
        $sample = ($newerEntities | Select-Object -First 5) -join ', '
        Add-Issue -Level 'WARNING' -Repo $repoName -Path 'items.lua' -Message ("{0} Entity companion новее items.lua; проверить editor round-trip. Примеры: {1}" -f $newerEntities.Count, $sample)
    }

    $repoIssues = @($script:issues | Where-Object { $_.Repo -eq $repoName })
    $repoErrors = @($repoIssues | Where-Object { $_.Level -in @('ERROR', 'FATAL') }).Count
    $repoWarnings = @($repoIssues | Where-Object { $_.Level -eq 'WARNING' }).Count
    Write-Output ("[{0}] metadata.code={1}; ModItem={2}; generated={3}; entities={4}; errors={5}; warnings={6}" -f $repoName, $codePaths.Count, $records.Count, $generated.Count, $entityFiles.Count, $repoErrors, $repoWarnings)
}

$displayBlocking = @($script:issues | Where-Object { $_.Level -in @('ERROR', 'FATAL') })
$displayWarnings = @($script:issues | Where-Object { $_.Level -eq 'WARNING' })
foreach ($issue in $displayBlocking) {
    Write-Output ("{0} [{1}] {2}: {3}" -f $issue.Level, $issue.Repo, $issue.Path, $issue.Message)
}
if ($DetailedWarnings -or $Strict) {
    foreach ($issue in $displayWarnings) {
        Write-Output ("{0} [{1}] {2}: {3}" -f $issue.Level, $issue.Repo, $issue.Path, $issue.Message)
    }
} else {
    foreach ($group in @($displayWarnings | Group-Object Repo)) {
        $examples = @($group.Group | Select-Object -First 3 | ForEach-Object { $_.Path }) -join ', '
        Write-Output ("WARNING SUMMARY [{0}] count={1}; examples: {2}" -f $group.Name, $group.Count, $examples)
    }
}

if ($script:fatal) {
    Write-Output 'RESULT: FAILED (core files or parser error)'
    exit 1
}

$blocking = @($script:issues | Where-Object { $_.Level -in @('ERROR', 'FATAL') })
$warnings = @($script:issues | Where-Object { $_.Level -eq 'WARNING' })
if ($blocking.Count -gt 0) {
    Write-Output ("RESULT: FAILED ({0} blocking issue(s), {1} warning(s))" -f $blocking.Count, $warnings.Count)
    exit 1
}

if ($warnings.Count -eq 0) {
    Write-Output 'RESULT: OK'
    exit 0
}

if ($Strict) {
    Write-Output ("RESULT: FAILED STRICT ({0} warning(s))" -f $warnings.Count)
    exit 2
}

Write-Output ("RESULT: WARNINGS ({0}); blocking errors are always fatal, use -Strict to reject warnings." -f $warnings.Count)
exit 0