[CmdletBinding()]
param(
    [string]$SuiteRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
)

$ErrorActionPreference = 'Stop'
$main = (Resolve-Path $SuiteRoot).Path
$parent = Split-Path $main -Parent
$roots = @(
    $main,
    (Join-Path $parent 'jazz_assets'),
    (Join-Path $parent 'jazz-assets'),
    (Join-Path $parent 'jazz-maps'),
    (Join-Path $parent 'jazz-units')
) | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -Unique

$docsRoot = Join-Path $main 'docs'
$technicalRoot = Join-Path $docsRoot 'technical'
$systemsRoot = Join-Path $technicalRoot 'systems'
$wikiRoot = Join-Path $docsRoot 'wiki'
$docsIndex = Join-Path $docsRoot 'README.md'
$technicalIndex = Join-Path $technicalRoot 'README.md'
$systemsIndex = Join-Path $systemsRoot 'README.md'
$wikiIndex = Join-Path $wikiRoot 'README.md'
$coverage = Join-Path $systemsRoot 'file-coverage.md'
$errors = [System.Collections.Generic.List[string]]::new()

foreach ($required in @($docsIndex, $technicalIndex, $systemsIndex, $wikiIndex, $coverage)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        $errors.Add("Не найден обязательный файл документации: $required")
    }
}
if ($errors.Count) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

$docsIndexText = Get-Content -LiteralPath $docsIndex -Raw
if ($docsIndexText -notmatch 'technical/README\.md' -or $docsIndexText -notmatch 'wiki/README\.md') {
    $errors.Add('docs/README.md должен вести и в technical, и в wiki.')
}

$systemsIndexText = Get-Content -LiteralPath $systemsIndex -Raw
$coverageText = Get-Content -LiteralPath $coverage -Raw
$systemPages = Get-ChildItem -LiteralPath $systemsRoot -File -Filter '*.md' |
    Where-Object { $_.Name -notin @('README.md', 'file-coverage.md') }
foreach ($page in $systemPages) {
    if ($systemsIndexText -notmatch [regex]::Escape($page.Name)) {
        $errors.Add("На системную страницу нет ссылки из technical/systems/README.md: $($page.Name)")
    }
}

$wikiIndexText = Get-Content -LiteralPath $wikiIndex -Raw
$wikiPages = Get-ChildItem -LiteralPath $wikiRoot -File -Filter '*.md' |
    Where-Object { $_.Name -ne 'README.md' }
foreach ($page in $wikiPages) {
    if ($wikiIndexText -notmatch [regex]::Escape($page.Name)) {
        $errors.Add("На wiki-страницу нет ссылки из docs/wiki/README.md: $($page.Name)")
    }
    $pageText = Get-Content -LiteralPath $page.FullName -Raw
    if ($pageText -notmatch '\.\./technical/') {
        $errors.Add("Wiki-страница не ссылается на technical-раздел: $($page.Name)")
    }
}

foreach ($root in $roots) {
    $codeRoot = Join-Path $root 'Code'
    if (-not (Test-Path -LiteralPath $codeRoot)) { continue }
    $files = Get-ChildItem -LiteralPath $codeRoot -Recurse -File -Filter '*.lua' |
        Where-Object { $_.Name -notmatch '^(FX_|CodeSounds)' }
    foreach ($file in $files) {
        if ($coverageText -notmatch [regex]::Escape($file.Name)) {
            $errors.Add("Для Code-файла нет записи в file-coverage.md: $($file.FullName)")
        }
    }
}

$markdown = Get-ChildItem -LiteralPath $main -Recurse -File -Filter '*.md' |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' }
foreach ($file in $markdown) {
    $lineNo = 0
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $lineNo++
        if ($line -match '(?i)\b[A-Z]:[\\/]') {
            $errors.Add("Абсолютный путь Windows в Markdown: $($file.FullName):$lineNo")
        }
        if ($line -match '[ \t]+$') {
            $errors.Add("Пробелы в конце строки: $($file.FullName):$lineNo")
        }
    }
}

if ($errors.Count) {
    $errors | Sort-Object -Unique | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host ("Документация в порядке: technical systems — {0}, wiki-гайдов — {1}, проверено репозиториев — {2}." -f $systemPages.Count, $wikiPages.Count, $roots.Count)
exit 0