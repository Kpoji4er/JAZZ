#Requires -Version 5.1
<#
.SYNOPSIS
  Собирает GitHub Wiki staging из docs/showcase + docs/wiki/weapons и опционально публикует.

.PARAMETER Publish
  Клонирует wiki-репозиторий и пушит собранные страницы.

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
$CatalogRoot = Join-Path $RepoRoot 'docs\wiki\weapons'
$WikiRoot = Join-Path $RepoRoot 'docs\wiki'
$ManifestPath = Join-Path $ShowcaseRoot 'pages.json'

if (-not $StagingDir) {
    $StagingDir = Join-Path $RepoRoot '.tmp\github-wiki'
}

function Get-RepoSlugFromOrigin {
    Push-Location $RepoRoot
    try {
        $url = (git remote get-url origin 2>$null)
        if (-not $url) { throw 'Cannot read git remote origin.' }
        if ($url -match 'github\.com[:/](?<slug>[^/]+/[^/.]+)') {
            return $Matches['slug']
        }
        throw "origin is not a GitHub URL: $url"
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

function Get-CatalogWikiPageName {
    param([string]$FileBase)
    if ($FileBase -eq 'README') { return 'Weapons-Catalog' }
    $parts = $FileBase -split '-'
    $title = ($parts | ForEach-Object {
            if ([string]::IsNullOrEmpty($_)) { return $_ }
            return $_.Substring(0, 1).ToUpperInvariant() + $_.Substring(1)
        }) -join '-'
    return "Weapons-$title"
}

function Get-MarkdownTitle {
    param([string]$Text, [string]$Fallback)
    foreach ($line in [regex]::Split($Text, '\r?\n')) {
        if ($line -match '^#\s+(.+)$') {
            return $Matches[1].Trim()
        }
    }
    return $Fallback
}

function Resolve-PublishedLink {
    param(
        [string]$FromFile,
        [string]$Target,
        [hashtable]$SlugToWikiBase,
        [string]$RepoSlug
    )

    $clean = ($Target -split '#', 2)[0].Trim()
    if ([string]::IsNullOrWhiteSpace($clean)) { return $null }
    if ($clean -match '^(https?://|mailto:)' -or $clean.StartsWith('#')) { return $null }

    $resolved = [IO.Path]::GetFullPath((Join-Path ([IO.Path]::GetDirectoryName($FromFile)) $clean))
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) {
        return $null
    }

    $ruRoot = [IO.Path]::GetFullPath((Join-Path $ShowcaseRoot 'ru'))
    $enRoot = [IO.Path]::GetFullPath((Join-Path $ShowcaseRoot 'en'))
    $catalogFull = [IO.Path]::GetFullPath($CatalogRoot)
    $wikiFull = [IO.Path]::GetFullPath($WikiRoot)
    $repoFull = [IO.Path]::GetFullPath($RepoRoot)

    if ($resolved.StartsWith($ruRoot, [StringComparison]::OrdinalIgnoreCase)) {
        $relative = $resolved.Substring($ruRoot.Length).TrimStart('\', '/')
        if (-not $relative.EndsWith('.md', [StringComparison]::OrdinalIgnoreCase)) { return $null }
        $slug = [IO.Path]::GetFileNameWithoutExtension($relative)
        if (-not $SlugToWikiBase.ContainsKey($slug)) {
            throw "Unknown showcase slug link: $Target (from $FromFile)"
        }
        return (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase[$slug])
    }

    if ($resolved.StartsWith($enRoot, [StringComparison]::OrdinalIgnoreCase)) {
        $relative = $resolved.Substring($enRoot.Length).TrimStart('\', '/')
        if (-not $relative.EndsWith('.md', [StringComparison]::OrdinalIgnoreCase)) { return $null }
        $slug = [IO.Path]::GetFileNameWithoutExtension($relative)
        if (-not $SlugToWikiBase.ContainsKey($slug)) {
            throw "Unknown showcase slug link: $Target (from $FromFile)"
        }
        return (Get-WikiPageName -Lang 'en' -WikiBase $SlugToWikiBase[$slug])
    }

    if ($resolved.StartsWith($catalogFull, [StringComparison]::OrdinalIgnoreCase)) {
        $relative = $resolved.Substring($catalogFull.Length).TrimStart('\', '/')
        if (-not $relative.EndsWith('.md', [StringComparison]::OrdinalIgnoreCase)) { return $null }
        $base = [IO.Path]::GetFileNameWithoutExtension($relative)
        return (Get-CatalogWikiPageName -FileBase $base)
    }

    # Root docs/wiki pages map onto showcase RU aspect pages where we already mirror them.
    $wikiPageMap = @{
        'weapons-and-ammo.md'     = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['weapons-and-ammo'])
        'combat-and-accuracy.md'  = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['combat-and-accuracy'])
        'weapon-classes.md'       = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['weapon-classes'])
        'combat-actions.md'       = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['combat-actions'])
        'legion-global-ai.md'     = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['legion-strategy'])
        'README.md'               = (Get-WikiPageName -Lang 'ru' -WikiBase $SlugToWikiBase['home'])
    }
    if ($resolved.StartsWith($wikiFull, [StringComparison]::OrdinalIgnoreCase)) {
        $relative = $resolved.Substring($wikiFull.Length).TrimStart('\', '/').Replace('\', '/')
        if ($wikiPageMap.ContainsKey($relative)) {
            return $wikiPageMap[$relative]
        }
    }

    if ($resolved.StartsWith($repoFull, [StringComparison]::OrdinalIgnoreCase)) {
        $relativePath = $resolved.Substring($repoFull.Length).TrimStart('\', '/').Replace('\', '/')
        if ($relativePath -match '\.(md|csv|lua)$') {
            return ("https://github.com/{0}/blob/main/{1}" -f $RepoSlug, $relativePath)
        }
    }

    return $null
}

function Rewrite-MarkdownLinks {
    param(
        [string]$Text,
        [string]$FromFile,
        [hashtable]$SlugToWikiBase,
        [string]$RepoSlug
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
            $wikiPage = Resolve-PublishedLink -FromFile $FromFile -Target $target -SlugToWikiBase $SlugToWikiBase -RepoSlug $RepoSlug
            if (-not $wikiPage) {
                return $m.Value
            }
            return ('[{0}]({1}{2})' -f $label, $wikiPage, $hash)
        })
}

if (-not $RepoSlug) {
    $RepoSlug = Get-RepoSlugFromOrigin
}

if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Missing manifest: $ManifestPath"
}
if (-not (Test-Path -LiteralPath $CatalogRoot -PathType Container)) {
    throw "Missing weapon catalog: $CatalogRoot"
}

$manifest = ConvertFrom-JsonFile -Path $ManifestPath
$order = @($manifest.order)
$pages = $manifest.pages
$slugToWikiBase = @{}
foreach ($slug in $order) {
    $entry = $pages.$slug
    if (-not $entry) { throw "pages.json: slug '$slug' is in order but missing from pages." }
    $slugToWikiBase[$slug] = [string]$entry.wikiBase
}

foreach ($lang in @('ru', 'en')) {
    $langDir = Join-Path $ShowcaseRoot $lang
    foreach ($slug in $order) {
        $path = Join-Path $langDir ($slug + '.md')
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Missing showcase page: docs/showcase/$lang/$slug.md"
        }
    }
}

$catalogFiles = @(Get-ChildItem -LiteralPath $CatalogRoot -File -Filter '*.md' | Sort-Object {
        if ($_.BaseName -eq 'README') { '0' }
        elseif ($_.BaseName -eq 'components') { '1' }
        else { '2' + $_.BaseName }
    })
if ($catalogFiles.Count -lt 1) {
    throw "No markdown files in $CatalogRoot"
}

if (Test-Path -LiteralPath $StagingDir) {
    Remove-Item -LiteralPath $StagingDir -Recurse -Force
}
New-Item -ItemType Directory -Path $StagingDir | Out-Null

$generated = New-Object System.Collections.Generic.List[string]
$catalogSidebar = New-Object System.Collections.Generic.List[object]

foreach ($lang in @('ru', 'en')) {
    $langDir = Join-Path $ShowcaseRoot $lang
    foreach ($slug in $order) {
        $src = Join-Path $langDir ($slug + '.md')
        $wikiName = Get-WikiPageName -Lang $lang -WikiBase $slugToWikiBase[$slug]
        $text = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
        $text = Rewrite-MarkdownLinks -Text $text -FromFile $src -SlugToWikiBase $slugToWikiBase -RepoSlug $RepoSlug
        if ($text -notmatch '\r?\n$') { $text += "`n" }
        $dest = Join-Path $StagingDir ($wikiName + '.md')
        [IO.File]::WriteAllText($dest, $text, [Text.UTF8Encoding]::new($false))
        $generated.Add($wikiName) | Out-Null
    }
}

foreach ($file in $catalogFiles) {
    $wikiName = Get-CatalogWikiPageName -FileBase $file.BaseName
    $text = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
    $title = Get-MarkdownTitle -Text $text -Fallback $file.BaseName
    $banner = @(
        '> Published from `docs/wiki/weapons/` (generated catalog). Numbers come from canonical CSV; do not edit this GitHub Wiki page by hand.'
        '>'
        "> [Showcase RU]($(Get-WikiPageName -Lang 'ru' -WikiBase $slugToWikiBase['weapons-and-ammo'])) · [Showcase EN]($(Get-WikiPageName -Lang 'en' -WikiBase $slugToWikiBase['weapons-and-ammo'])) · [Full catalog index](Weapons-Catalog)"
        ''
    ) -join "`n"
    if ($text -match '(?s)\A(<!--.*?-->\r?\n)') {
        $text = $Matches[1] + $banner + $text.Substring($Matches[1].Length)
    }
    else {
        $text = $banner + $text
    }
    $text = Rewrite-MarkdownLinks -Text $text -FromFile $file.FullName -SlugToWikiBase $slugToWikiBase -RepoSlug $RepoSlug
    if ($text -notmatch '\r?\n$') { $text += "`n" }
    $dest = Join-Path $StagingDir ($wikiName + '.md')
    [IO.File]::WriteAllText($dest, $text, [Text.UTF8Encoding]::new($false))
    $generated.Add($wikiName) | Out-Null
    $catalogSidebar.Add([pscustomobject]@{ Name = $wikiName; Title = $title }) | Out-Null
}

$homeRu = Get-WikiPageName -Lang 'ru' -WikiBase $slugToWikiBase['home']
$homeEn = Get-WikiPageName -Lang 'en' -WikiBase $slugToWikiBase['home']
$rootHome = @"
# JAZZ

Player-facing showcase for the JAZZ overhaul of Jagged Alliance 3.

- [Русский]($homeRu)
- [English]($homeEn)
- [Weapon catalog / Каталог оружия](Weapons-Catalog)

Source of truth: ``docs/showcase/`` + generated ``docs/wiki/weapons/`` in the [JAZZ](https://github.com/$RepoSlug) repository. Do not edit wiki pages by hand — change the repo and republish.
"@
[IO.File]::WriteAllText((Join-Path $StagingDir 'Home.md'), ($rootHome.TrimEnd() + "`n"), [Text.UTF8Encoding]::new($false))

$sidebarLines = New-Object System.Collections.Generic.List[string]
$sidebarLines.Add('**JAZZ**') | Out-Null
$sidebarLines.Add('') | Out-Null
$sidebarLines.Add('- [Home](Home)') | Out-Null
$sidebarLines.Add('- [Weapon catalog](Weapons-Catalog)') | Out-Null
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
$sidebarLines.Add('**Каталог оружия**') | Out-Null
foreach ($item in $catalogSidebar) {
    $sidebarLines.Add(('- [{0}]({1})' -f $item.Title, $item.Name)) | Out-Null
}
$sidebarLines.Add('') | Out-Null
[IO.File]::WriteAllText((Join-Path $StagingDir '_Sidebar.md'), (($sidebarLines -join "`n") + "`n"), [Text.UTF8Encoding]::new($false))

$footer = @"
---
Published from ``docs/showcase/`` + ``docs/wiki/weapons/`` · [Repository](https://github.com/$RepoSlug) · [ADR-0003](https://github.com/$RepoSlug/blob/main/docs/decisions/ADR-0003-github-wiki-showcase.md)
"@
[IO.File]::WriteAllText((Join-Path $StagingDir '_Footer.md'), ($footer.TrimEnd() + "`n"), [Text.UTF8Encoding]::new($false))

Write-Host ("Wiki staging ready: {0} pages -> {1}" -f $generated.Count, $StagingDir)

if (-not $Publish) {
    exit 0
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
    git commit -m "sync showcase + weapon catalog" 2>&1 | ForEach-Object { Write-Host $_ }
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
