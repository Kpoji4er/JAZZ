[CmdletBinding()]
param(
    [string]$SuiteRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path,
    [string[]]$Paths
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$errors = [System.Collections.Generic.List[string]]::new()

function Add-DocError {
    param([string]$Message)
    $script:errors.Add($Message) | Out-Null
}

$main = (Resolve-Path $SuiteRoot).Path
$parent = Split-Path $main -Parent
$roots = @(
    @(
        $main,
        (Join-Path $parent 'jazz_assets'),
        (Join-Path $parent 'jazz-assets'),
        (Join-Path $parent 'jazz-maps'),
        (Join-Path $parent 'jazz-units')
    ) | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -Unique
)

$localMode = $PSBoundParameters.ContainsKey('Paths')
$selected = @()
$systemPages = @()
if ($localMode) {
    if (-not $Paths -or $Paths.Count -eq 0) { Add-DocError '-Paths требует хотя бы один файл.' }
    foreach ($relative in $Paths) {
        $candidate = [IO.Path]::GetFullPath((Join-Path $main $relative))
        if ([IO.Path]::IsPathRooted($relative) -or -not $candidate.StartsWith($main.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
            Add-DocError "Путь вне репозитория: $relative"
        } elseif (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            Add-DocError "Не найден выбранный файл: $relative"
        } elseif ($candidate -notmatch '(?i)\.md$|[\\/]agents[\\/]openai\.yaml$') {
            Add-DocError "Неподдерживаемый тип документа: $relative"
        } else { $selected += Get-Item -LiteralPath $candidate }
    }
    Write-Host 'Documentation scope: local; global coverage/index/showcase checks NOT RUN.'
} else {
Write-Host 'Documentation scope: full.'
$required = @(
    'docs/README.md',
    'docs/specs/README.md',
    'docs/specs/_template/change.md',
    'docs/decisions/README.md',
    'docs/ownership/README.md',
    'docs/ownership/exclusive-resources.yaml',
    'docs/technical/README.md',
    'docs/technical/systems/README.md',
    'docs/technical/systems/file-coverage.md'
)
foreach ($relative in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $main $relative) -PathType Leaf)) {
        Add-DocError "Не найден обязательный файл: $relative"
    }
}
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ -ErrorAction Continue }
    exit 1
}

$docsIndex = Join-Path $main 'docs/README.md'
$docsIndexText = [IO.File]::ReadAllText($docsIndex, [Text.Encoding]::UTF8)
foreach ($target in @('specs/README.md', 'decisions/README.md', 'ownership/README.md', 'technical/README.md', 'wiki/README.md', 'showcase/README.md')) {
    if ($docsIndexText -notmatch [regex]::Escape($target)) {
        Add-DocError "docs/README.md не ведёт к $target."
    }
}

$showcaseRoot = Join-Path $main 'docs/showcase'
$showcaseManifest = Join-Path $showcaseRoot 'pages.json'
$showcaseReadme = Join-Path $showcaseRoot 'README.md'
if (-not (Test-Path -LiteralPath $showcaseReadme -PathType Leaf)) {
    Add-DocError 'Не найден обязательный файл: docs/showcase/README.md'
}
if (-not (Test-Path -LiteralPath $showcaseManifest -PathType Leaf)) {
    Add-DocError 'Не найден обязательный файл: docs/showcase/pages.json'
}
else {
    try {
        $showcase = [IO.File]::ReadAllText($showcaseManifest, [Text.Encoding]::UTF8) | ConvertFrom-Json
        $order = @($showcase.order)
        if ($order.Count -lt 1) {
            Add-DocError 'docs/showcase/pages.json: пустой order.'
        }
        foreach ($slug in $order) {
            $entry = $showcase.pages.$slug
            if (-not $entry) {
                Add-DocError "docs/showcase/pages.json: slug '$slug' есть в order, но нет в pages."
                continue
            }
            foreach ($prop in @('wikiBase', 'ru', 'en')) {
                if (-not $entry.$prop) {
                    Add-DocError "docs/showcase/pages.json: у '$slug' нет поля $prop."
                }
            }
            foreach ($lang in @('ru', 'en')) {
                $pagePath = Join-Path $showcaseRoot "$lang/$slug.md"
                if (-not (Test-Path -LiteralPath $pagePath -PathType Leaf)) {
                    Add-DocError "Нет страницы showcase: docs/showcase/$lang/$slug.md"
                }
            }
        }
        foreach ($lang in @('ru', 'en')) {
            $langDir = Join-Path $showcaseRoot $lang
            if (-not (Test-Path -LiteralPath $langDir -PathType Container)) { continue }
            $extra = @(Get-ChildItem -LiteralPath $langDir -File -Filter '*.md' |
                Where-Object { $order -notcontains [IO.Path]::GetFileNameWithoutExtension($_.Name) })
            foreach ($file in $extra) {
                Add-DocError ("Страница showcase не описана в pages.json order: docs/showcase/{0}/{1}" -f $lang, $file.Name)
            }
        }
    }
    catch {
        Add-DocError ("Не удалось разобрать docs/showcase/pages.json: {0}" -f $_.Exception.Message)
    }
}

$publishScript = Join-Path $main 'scripts/docs/publish-github-wiki.ps1'
if (-not (Test-Path -LiteralPath $publishScript -PathType Leaf)) {
    Add-DocError 'Не найден scripts/docs/publish-github-wiki.ps1'
}

$systemsRoot = Join-Path $main 'docs/technical/systems'
$systemsIndex = Join-Path $systemsRoot 'README.md'
$systemsIndexText = [IO.File]::ReadAllText($systemsIndex, [Text.Encoding]::UTF8)
$coverage = Join-Path $systemsRoot 'file-coverage.md'
$coverageText = [IO.File]::ReadAllText($coverage, [Text.Encoding]::UTF8)
$systemPages = @(Get-ChildItem -LiteralPath $systemsRoot -File -Filter '*.md' |
    Where-Object { $_.Name -notin @('README.md', 'file-coverage.md') })
foreach ($page in $systemPages) {
    if ($systemsIndexText -notmatch [regex]::Escape($page.Name)) {
        Add-DocError "На системную страницу нет ссылки из systems/README.md: $($page.Name)"
    }
}

foreach ($root in $roots) {
    $codeRoot = Join-Path $root 'Code'
    if (-not (Test-Path -LiteralPath $codeRoot -PathType Container)) { continue }
    $files = @(Get-ChildItem -LiteralPath $codeRoot -Recurse -File -Filter '*.lua' |
        Where-Object { $_.Name -notmatch '^(FX_|CodeSounds)' })
    foreach ($file in $files) {
        if ($coverageText -notmatch [regex]::Escape($file.Name)) {
            Add-DocError "Для Code-файла нет записи в file-coverage.md: $($file.FullName)"
        }
    }
}

}

$markdownRoots = @(
    (Join-Path $main 'docs'),
    (Join-Path $main '.agents')
)
$markdown = if ($localMode) { @($selected | Where-Object { $_.Extension -eq '.md' }) } else { $allMarkdown = @($markdownRoots | ForEach-Object {
    Get-ChildItem -LiteralPath $_ -Recurse -File -Filter '*.md'
})
$rootAgents = Join-Path $main 'AGENTS.md'
if (Test-Path -LiteralPath $rootAgents -PathType Leaf) {
    $allMarkdown += Get-Item -LiteralPath $rootAgents
}
$allMarkdown
}

$markdown = @($markdown)
foreach ($file in $markdown) {
    $relativeSource = $file.FullName.Substring($main.Length).TrimStart('\', '/').Replace('\', '/')
    $text = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
    $lineNo = 0
    foreach ($line in [regex]::Split($text, '\r?\n')) {
        $lineNo++
        if ($line -match '(?i)\b[A-Z]:[\\/]') {
            Add-DocError "Абсолютный путь Windows: ${relativeSource}:$lineNo"
        }
        if ($line -match '[ \t]+$') {
            Add-DocError "Пробелы в конце строки: ${relativeSource}:$lineNo"
        }
    }

    foreach ($match in [regex]::Matches($text, '\[[^\]]*\]\((?<target>[^)]+)\)')) {
        $target = $match.Groups['target'].Value.Trim().Trim('<', '>')
        if ($target -match '^https?://' -or $target -match '^mailto:' -or $target.StartsWith('#')) { continue }
        $target = ($target -split '#', 2)[0]
        if ([string]::IsNullOrWhiteSpace($target)) { continue }
        try {
            $resolvedTarget = [IO.Path]::GetFullPath((Join-Path $file.DirectoryName $target))
        } catch {
            Add-DocError "Некорректная ссылка: $relativeSource -> $target"
            continue
        }
        if (-not (Test-Path -LiteralPath $resolvedTarget)) {
            Add-DocError "Сломанная внутренняя ссылка: $relativeSource -> $target"
        }
    }
}

$skillRoot = Join-Path $main '.agents/skills'
$skills = if ($localMode) {
    @($selected | ForEach-Object {
        $rel = $_.FullName.Substring($main.Length).Replace('\', '/')
        if ($rel -match '^/\.agents/skills/(?<name>[^/]+)/') {
            Get-Item -LiteralPath (Join-Path $skillRoot $Matches['name'])
        }
    } | Sort-Object -Property FullName -Unique)
} elseif (Test-Path -LiteralPath $skillRoot) { @(Get-ChildItem -LiteralPath $skillRoot -Directory) } else { @() }
$skills = @($skills)
foreach ($skill in $skills) {
    $skillFile = Join-Path $skill.FullName 'SKILL.md'
    $agentFile = Join-Path $skill.FullName 'agents/openai.yaml'
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        Add-DocError "Skill без SKILL.md: $($skill.Name)"
        continue
    }
    $skillText = [IO.File]::ReadAllText($skillFile, [Text.Encoding]::UTF8)
    $frontmatter = [regex]::Match($skillText, '(?s)\A---\s*\r?\n(?<yaml>.*?)\r?\n---')
    if (-not $frontmatter.Success -or
        $frontmatter.Groups['yaml'].Value -notmatch '(?m)^name:\s*[a-z0-9-]+\s*$' -or
        $frontmatter.Groups['yaml'].Value -notmatch '(?m)^description:\s*\S.+$') {
        Add-DocError "Некорректный frontmatter skill: $($skill.Name)"
    }
    if ($skillText -match '\[TODO' -or $skillText.IndexOf([char]0x045F) -ge 0 -or $skillText.IndexOf([char]0x0402) -ge 0 -or $skillText.IndexOf([char]0x0403) -ge 0) {
        Add-DocError "Skill содержит TODO или признаки mojibake: $($skill.Name)"
    }
    if (Test-Path -LiteralPath $agentFile -PathType Leaf) {
        $agentText = [IO.File]::ReadAllText($agentFile, [Text.Encoding]::UTF8)
        if ($agentText -notmatch '(?m)^interface:\s*$' -or $agentText -notmatch ('(?m)^  default_prompt:.*' + [regex]::Escape('$' + $skill.Name))) {
            Add-DocError ("default_prompt не упоминает {0}: {1}" -f ('$' + $skill.Name), $skill.Name)
        }
        if ($agentText.Contains([char]0xFFFD)) {
            Add-DocError "agents/openai.yaml содержит replacement characters: $($skill.Name)"
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | Sort-Object -Unique | ForEach-Object { Write-Error $_ -ErrorAction Continue }
    exit 1
}

Write-Host ("Documentation contract passed: systems={0}, skills={1}, markdown={2}, repos={3}." -f $systemPages.Count, $skills.Count, $markdown.Count, $roots.Count)
exit 0
