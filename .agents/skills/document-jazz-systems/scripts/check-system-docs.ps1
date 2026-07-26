[CmdletBinding()]
param(
    [string]$SuiteRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
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
foreach ($target in @('specs/README.md', 'decisions/README.md', 'ownership/README.md', 'technical/README.md')) {
    if ($docsIndexText -notmatch [regex]::Escape($target)) {
        Add-DocError "docs/README.md не ведёт к $target."
    }
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

$markdownRoots = @(
    (Join-Path $main 'docs'),
    (Join-Path $main '.agents')
)
$markdown = @($markdownRoots | ForEach-Object {
    Get-ChildItem -LiteralPath $_ -Recurse -File -Filter '*.md'
})
$rootAgents = Join-Path $main 'AGENTS.md'
if (Test-Path -LiteralPath $rootAgents -PathType Leaf) {
    $markdown += Get-Item -LiteralPath $rootAgents
}

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
        if ($target -match '(?i)(?:^|[\\/])docs[\\/]wiki[\\/]' -or $target -match '(?i)(?:^|[\\/])wiki[\\/]') {
            Add-DocError "Ссылка на отключённую wiki: $relativeSource -> $target"
            continue
        }
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
$skills = @(Get-ChildItem -LiteralPath $skillRoot -Directory)
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
    if (-not (Test-Path -LiteralPath $agentFile -PathType Leaf)) {
        Add-DocError "Skill без agents/openai.yaml: $($skill.Name)"
    } else {
        $agentText = [IO.File]::ReadAllText($agentFile, [Text.Encoding]::UTF8)
        if ($agentText -notmatch [regex]::Escape('$' + $skill.Name)) {
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
