#Requires -Version 5.1
<#
.SYNOPSIS
  Собирает GitHub Wiki staging из docs/showcase и опционально публикует в JAZZ.wiki.

.PARAMETER Publish
  Клонирует/создаёт wiki-репозиторий и пушит собранные страницы.

.PARAMETER StagingDir
  Каталог сборки (по умолчанию .tmp/github-wiki).

.PARAMETER RepoSlug
  owner/name репозитория с wiki (по умолчанию из git remote origin).

.PARAMETER DryRunPublish
  При -Publish не пушить, только показать статус staging/clone.
#>
[CmdletBinding()]
param(
    [switch]$Publish,
    [switch]$DryRunPublish,
    [string]$StagingDir = '',
    [string]$RepoSlug = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ScriptDir = $PSScriptRoot
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path
$ShowcaseRoot = Join-Path $RepoRoot 'docs\showcase'
$ManifestPath = Join-Path $ShowcaseRoot 'pages.json'

if (-not $StagingDir) {
    $StagingDir = Join-Path $RepoRoot '.tmp\github-wiki'
}

function Get-RepoSlugFromOrigin {
    Push-Location $RepoRoot
    try {
        $url = (git remote get-url origin 2>$null)
        if (-not $url) { throw 'Не удалось прочитать git remote origin.' }
        if ($url -match 'github\.com[:/](?<slug>[^/]+/[^/.]+)') {
            return $Matches['slug']
        }
        throw "origin не похож на GitHub URL: $url"
    }
    finally {
        Pop-Location
    }
}

function ConvertFrom-JsonFile {
    param([string]$Path)
    $raw = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
    return ($raw | ConvertFrom-Json)
}

function Get-WikiPageName {
    param(
        [string]$Lang,
        [string]$WikiBase
    )
    return ('{0}-{1}' -f $Lang.ToUpperInvariant(), $WikiBase)
}

function Resolve-ShowcaseLinkTarget {
    param(
        [string]$FromFile,
        [string]$Target,
        [hashtable]$SlugToWikiBase,
        [string]$Lang
    )

    $clean = ($Target -split '#', 2)[0].Trim()
    if ([string]::IsNullOrWhiteSpace($clean)) { return $null }
    if ($clean -match '^(https?://|mailto:)' -or $clean.StartsWith('#')) { return $null }

    $resolved = [IO.Path]::GetFullPath((Join-Path ([IO.Path]::GetDirectoryName($FromFile)) $clean))
    $ruRoot = [IO.Path]::GetFullPath((Join-Path $ShowcaseRoot 'ru'))
    $enRoot = [IO.Path]::GetFullPath((Join-Path $ShowcaseRoot 'en'))

    $targetLang = $null
    $relative = $null
    if ($resolved.StartsWith($ruRoot, [StringComparison]::OrdinalIgnoreCase)) {
        $targetLang = 'ru'
        $relative = $resolved.Substring($ruRoot.Length).TrimStart('\', '/')
    }
    elseif ($resolved.StartsWith($enRoot, [StringComparison]::OrdinalIgnoreCase)) {
        $targetLang = 'en'
        $relative = $resolved.Substring($enRoot.Length).TrimStart('\', '/')
    }
    else {
        return $null
    }

    if (-not $relative.EndsWith('.md', [StringComparison]::OrdinalIgnoreCase)) {
        return $null
    }

    $slug = [IO.Path]::GetFileNameWithoutExtension($relative).Replace('\', '/')
    if (-not $SlugToWikiBase.ContainsKey($slug)) {
        throw "Ссылка на неизвестный slug showcase: $Target (из $FromFile)"
    }

    return (Get-WikiPageName -Lang $targetLang -WikiBase $SlugToWikiBase[$slug])
}

function Rewrite-MarkdownLinks {
    param(
        [string]$Text,
        [string]$FromFile,
        [hashtable]$SlugToWikiBase,
        [string]$Lang
    )

    return [regex]::Replace($Text, '\[(?<label>[^\]]*)\]\((?<target>[^)]+)\)', {
        param($m)
        $label = $m.Groups['label'].Value
        $target = $m.Groups['target'].Value.Trim()
        $hash = ''
        if ($target.Contains('#')) {
            $parts = $target -split '#', 2
            $target = $parts[0]
            $hash = '#' + $parts[1]
        }
        $wikiPage = Resolve-ShowcaseLinkTarget -FromFile $FromFile -Target $target -SlugToWikiBase $SlugToWikiBase -Lang $Lang
        if (-not $wikiPage) {
            return $m.Value
        }
        return ('[{0}]({1}{2})' -f $label, $wikiPage, $hash)
    })
}

if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Нет манифеста: $ManifestPath"
}

$manifest = ConvertFrom-JsonFile -Path $ManifestPath
$order = @($manifest.order)
$pages = $manifest.pages
$slugToWikiBase = @{}
foreach ($slug in $order) {
    $entry = $pages.$slug
    if (-not $entry) { throw "pages.json: slug '$slug' есть в order, но нет в pages." }
    $slugToWikiBase[$slug] = [string]$entry.wikiBase
}

foreach ($lang in @('ru', 'en')) {
    $langDir = Join-Path $ShowcaseRoot $lang
    foreach ($slug in $order) {
        $path = Join-Path $langDir ($slug + '.md')
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Нет страницы showcase: docs/showcase/$lang/$slug.md"
        }
    }
}

if (Test-Path -LiteralPath $StagingDir) {
    Remove-Item -LiteralPath $StagingDir -Recurse -Force
}
New-Item -ItemType Directory -Path $StagingDir | Out-Null

$generated = New-Object System.Collections.Generic.List[string]

foreach ($lang in @('ru', 'en')) {
    $langDir = Join-Path $ShowcaseRoot $lang
    foreach ($slug in $order) {
        $src = Join-Path $langDir ($slug + '.md')
        $wikiBase = $slugToWikiBase[$slug]
        $wikiName = Get-WikiPageName -Lang $lang -WikiBase $wikiBase
        $text = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
        $text = Rewrite-MarkdownLinks -Text $text -FromFile $src -SlugToWikiBase $slugToWikiBase -Lang $lang
        if ($text -notmatch '\r?\n$') { $text += "`n" }
        $dest = Join-Path $StagingDir ($wikiName + '.md')
        [IO.File]::WriteAllText($dest, $text, [Text.UTF8Encoding]::new($false))
        $generated.Add($wikiName) | Out-Null
    }
}

$homeRu = Get-WikiPageName -Lang 'ru' -WikiBase $slugToWikiBase['home']
$homeEn = Get-WikiPageName -Lang 'en' -WikiBase $slugToWikiBase['home']
$rootHome = @"
# JAZZ

Player-facing showcase for the JAZZ overhaul of Jagged Alliance 3.

- [Русский]($homeRu)
- [English]($homeEn)

Source of truth: ``docs/showcase/`` in the [JAZZ](https://github.com/Kpoji4er/JAZZ) repository. Do not edit wiki pages by hand — change the repo and republish.
"@
[IO.File]::WriteAllText((Join-Path $StagingDir 'Home.md'), ($rootHome.TrimEnd() + "`n"), [Text.UTF8Encoding]::new($false))

$sidebarLines = New-Object System.Collections.Generic.List[string]
$sidebarLines.Add('**JAZZ**') | Out-Null
$sidebarLines.Add('') | Out-Null
$sidebarLines.Add('- [Home](Home)') | Out-Null
$sidebarLines.Add('') | Out-Null
$sidebarLines.Add('**Русский**') | Out-Null
foreach ($slug in $order) {
    $title = [string]$pages.$slug.ru
    $page = Get-WikiPageName -Lang 'ru' -WikiBase $slugToWikiBase[$slug]
    $sidebarLines.Add(('- [{0}]({1})' -f $title, $page)) | Out-Null
}
$sidebarLines.Add('') | Out-Null
$sidebarLines.Add('**English**') | Out-Null
foreach ($slug in $order) {
    $title = [string]$pages.$slug.en
    $page = Get-WikiPageName -Lang 'en' -WikiBase $slugToWikiBase[$slug]
    $sidebarLines.Add(('- [{0}]({1})' -f $title, $page)) | Out-Null
}
$sidebarLines.Add('') | Out-Null
[IO.File]::WriteAllText((Join-Path $StagingDir '_Sidebar.md'), (($sidebarLines -join "`n") + "`n"), [Text.UTF8Encoding]::new($false))

$footer = @"
---
Published from ``docs/showcase/`` · [Repository](https://github.com/Kpoji4er/JAZZ) · [ADR-0003](https://github.com/Kpoji4er/JAZZ/blob/main/docs/decisions/ADR-0003-github-wiki-showcase.md)
"@
[IO.File]::WriteAllText((Join-Path $StagingDir '_Footer.md'), ($footer.TrimEnd() + "`n"), [Text.UTF8Encoding]::new($false))

Write-Host ("Showcase wiki staging ready: {0} pages -> {1}" -f $generated.Count, $StagingDir)

if (-not $Publish) {
    exit 0
}

if (-not $RepoSlug) {
    $RepoSlug = Get-RepoSlugFromOrigin
}

$wikiUrl = "https://github.com/${RepoSlug}.wiki.git"
$token = $env:GITHUB_TOKEN
if (-not $token) { $token = $env:GH_TOKEN }

$cloneDir = Join-Path $RepoRoot '.tmp\github-wiki-repo'
if (Test-Path -LiteralPath $cloneDir) {
    Remove-Item -LiteralPath $cloneDir -Recurse -Force
}

$authUrl = $wikiUrl
if ($token) {
    $authUrl = "https://x-access-token:${token}@github.com/${RepoSlug}.wiki.git"
}

$prevEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$cloneOutput = @(git clone --depth 1 $authUrl $cloneDir 2>&1)
$cloneCode = $LASTEXITCODE
$ErrorActionPreference = $prevEap
$cloneOutput | ForEach-Object { Write-Host $_ }
$cloneOk = ($cloneCode -eq 0) -and (Test-Path -LiteralPath (Join-Path $cloneDir '.git'))

if (-not $cloneOk) {
    if (Test-Path -LiteralPath $cloneDir) {
        Remove-Item -LiteralPath $cloneDir -Recurse -Force
    }
    Write-Host "Wiki clone failed or empty — initializing new wiki repo at $cloneDir"
    New-Item -ItemType Directory -Path $cloneDir -Force | Out-Null
    Push-Location $cloneDir
    try {
        $ErrorActionPreference = 'Continue'
        git init 2>&1 | ForEach-Object { Write-Host $_ }
        git checkout -b master 2>&1 | ForEach-Object { Write-Host $_ }
        git remote add origin $authUrl 2>&1 | ForEach-Object { Write-Host $_ }
        $ErrorActionPreference = 'Stop'
    }
    finally {
        Pop-Location
    }
}

Get-ChildItem -LiteralPath $cloneDir -Force |
    Where-Object { $_.Name -ne '.git' } |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

Copy-Item -Path (Join-Path $StagingDir '*') -Destination $cloneDir -Force

Push-Location $cloneDir
try {
    git config user.email '41898282+github-actions[bot]@users.noreply.github.com' | Out-Null
    git config user.name 'github-actions[bot]' | Out-Null
    $prevEap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    git add -A 2>&1 | ForEach-Object { Write-Host $_ }
    $status = git status --porcelain
    if (-not $status) {
        $ErrorActionPreference = $prevEap
        Write-Host 'GitHub Wiki already up to date.'
        exit 0
    }
    git commit -m "sync showcase from docs/showcase" 2>&1 | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) {
        $ErrorActionPreference = $prevEap
        throw 'git commit failed'
    }
    if ($DryRunPublish) {
        $ErrorActionPreference = $prevEap
        Write-Host 'DryRunPublish: commit created locally, push skipped.'
        exit 0
    }
    git push -u origin HEAD:master 2>&1 | ForEach-Object { Write-Host $_ }
    if ($LASTEXITCODE -ne 0) {
        $ErrorActionPreference = $prevEap
        Write-Host ''
        Write-Host 'Bootstrap required: GitHub creates *.wiki.git only after the first page exists.'
        Write-Host ("1. Open https://github.com/{0}/wiki and click Create the first page (title Home, any body)." -f $RepoSlug)
        Write-Host '2. Save the page.'
        Write-Host '3. Re-run: scripts/docs/publish-github-wiki.ps1 -Publish'
        throw 'git push to wiki failed'
    }
    $ErrorActionPreference = $prevEap
    Write-Host "Published GitHub Wiki: https://github.com/${RepoSlug}/wiki"
}
finally {
    Pop-Location
}
