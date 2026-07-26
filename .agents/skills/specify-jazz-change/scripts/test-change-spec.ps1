[CmdletBinding()]
param(
    [string]$Path = 'docs/specs',
    [ValidateSet('Schema', 'Ready', 'Done', 'All')]
    [string]$Phase = 'All'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$errors = [System.Collections.Generic.List[string]]::new()

function Add-SpecError {
    param([string]$File, [string]$Message)
    $script:errors.Add("${File}: $Message") | Out-Null
}

function Get-Scalar {
    param([string]$Yaml, [string]$Name)
    $match = [regex]::Match($Yaml, "(?m)^$([regex]::Escape($Name)):\s*(?<value>[^\r\n#]+)")
    if (-not $match.Success) { return '' }
    return $match.Groups['value'].Value.Trim().Trim('"', "'")
}

function Has-ListValue {
    param([string]$Yaml, [string]$Name)
    $escaped = [regex]::Escape($Name)
    return [regex]::IsMatch($Yaml, "(?m)^${escaped}:\s*\[[^\]]+\]\s*$") -or
        [regex]::IsMatch($Yaml, "(?ms)^${escaped}:\s*\r?\n(?:[ \t]+-[ \t]+[^\r\n]+\r?\n?)+")
}

function Has-Heading {
    param([string]$Body, [string]$Pattern)
    return [regex]::IsMatch($Body, "(?mi)^##[ \t]+(?:$Pattern)[ \t]*\r?$")
}

$resolved = Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue
if (-not $resolved) {
    Write-Error "Spec path не найден: $Path" -ErrorAction Continue
    exit 1
}

$item = Get-Item -LiteralPath $resolved.Path
$files = if ($item.PSIsContainer) {
    @(Get-ChildItem -LiteralPath $item.FullName -Recurse -File -Filter '*.md' |
        Where-Object {
            $_.Name -ne 'README.md' -and
            $_.FullName -notmatch '[\\/]_template[\\/]'
        })
} else {
    @($item)
}

foreach ($file in $files) {
    $relative = $file.FullName.Substring((Get-Location).Path.Length).TrimStart('\', '/').Replace('\', '/')
    $text = [IO.File]::ReadAllText($file.FullName, [Text.Encoding]::UTF8)
    $frontmatter = [regex]::Match($text, '(?s)\A---\s*\r?\n(?<yaml>.*?)\r?\n---\s*\r?\n(?<body>.*)\z')
    if (-not $frontmatter.Success) {
        Add-SpecError $relative 'отсутствует корректный YAML frontmatter.'
        continue
    }

    $yaml = $frontmatter.Groups['yaml'].Value
    $body = $frontmatter.Groups['body'].Value
    $id = Get-Scalar $yaml 'id'
    $status = Get-Scalar $yaml 'status'
    $owner = Get-Scalar $yaml 'owner'
    $risk = Get-Scalar $yaml 'risk'
    $generatedData = Get-Scalar $yaml 'generated_data'
    $runtimeValidation = Get-Scalar $yaml 'runtime_validation'
    $approvedBy = Get-Scalar $yaml 'approved_by'

    if ($id -notmatch '^JAZZ-[A-Z0-9][A-Z0-9-]*-\d{3}$') {
        Add-SpecError $relative "некорректный id '$id'."
    }
    if ($status -notin @('draft', 'approved', 'implemented', 'accepted', 'superseded')) {
        Add-SpecError $relative "некорректный status '$status'."
    }
    if ([string]::IsNullOrWhiteSpace($owner)) {
        Add-SpecError $relative 'не указан owner.'
    }
    if ($risk -notin @('low', 'medium', 'high', 'critical')) {
        Add-SpecError $relative "некорректный risk '$risk'."
    }
    if ($generatedData -notin @('true', 'false')) {
        Add-SpecError $relative "generated_data должен быть true или false, найдено '$generatedData'."
    }
    if ($runtimeValidation -notin @('required', 'not-required')) {
        Add-SpecError $relative "runtime_validation должен быть required или not-required, найдено '$runtimeValidation'."
    }
    foreach ($listName in @('systems', 'repositories', 'write_set', 'exclusive_resources')) {
        if (-not (Has-ListValue $yaml $listName)) {
            Add-SpecError $relative "не заполнен список $listName."
        }
    }

    $requiredHeadings = [ordered]@{
        'Проблема' = 'Проблема'
        'Цели' = 'Цели'
        'Non-goals' = 'Non-goals'
        'Требования' = 'Требования'
        'Инварианты' = 'Инварианты и ограничения'
        'Acceptance' = 'Acceptance criteria'
        'Impact' = 'Impact и совместимость'
        'Ownership' = 'План и ownership'
        'Решение' = 'Решение владельца'
        'Evidence' = 'Evidence'
        'Documentation' = 'Documentation delta'
    }
    foreach ($heading in $requiredHeadings.GetEnumerator()) {
        if (-not (Has-Heading $body ([regex]::Escape($heading.Value)))) {
            Add-SpecError $relative "отсутствует раздел '## $($heading.Value)'."
        }
    }

    if ($id) {
        $requirements = @([regex]::Matches($body, "\b$([regex]::Escape($id))-REQ-\d{3}\b") | ForEach-Object { $_.Value } | Sort-Object -Unique)
        $acceptance = @([regex]::Matches($body, "\b$([regex]::Escape($id))-AC-\d{3}\b") | ForEach-Object { $_.Value } | Sort-Object -Unique)
        if ($requirements.Count -eq 0) { Add-SpecError $relative 'нет ни одного REQ-ID.' }
        if ($acceptance.Count -eq 0) { Add-SpecError $relative 'нет ни одного AC-ID.' }
    } else {
        $requirements = @()
        $acceptance = @()
    }

    $effectivePhase = $Phase
    if ($Phase -eq 'All') {
        $effectivePhase = switch ($status) {
            'draft' { 'Schema' }
            'approved' { 'Ready' }
            'implemented' { 'Done' }
            'accepted' { 'Done' }
            'superseded' { 'Schema' }
            default { 'Schema' }
        }
    }

    if ($effectivePhase -in @('Ready', 'Done')) {
        if ($status -notin @('approved', 'implemented', 'accepted')) {
            Add-SpecError $relative "phase $effectivePhase требует status approved, implemented или accepted."
        }
        if ([string]::IsNullOrWhiteSpace($approvedBy) -or $approvedBy -in @('pending', 'none')) {
            Add-SpecError $relative 'DoR требует approved_by.'
        }
        if ([regex]::IsMatch($body, '(?i)\b(?:TBD|TODO)\b')) {
            Add-SpecError $relative 'approved spec содержит TBD/TODO.'
        }
    }

    if ($effectivePhase -eq 'Done') {
        if ($status -notin @('implemented', 'accepted')) {
            Add-SpecError $relative 'DoD требует status implemented или accepted.'
        }
        foreach ($ac in $acceptance) {
            $evidencePattern = '(?mi)^[-*][ \t]+`?' + [regex]::Escape($ac) + '`?:.*`?PASS`?\b'
            if (-not [regex]::IsMatch($body, $evidencePattern)) {
                Add-SpecError $relative "для $ac нет evidence со статусом PASS."
            }
        }
        if ([regex]::IsMatch($body, '(?mi)^[-*].*`?(?:FAIL|BLOCKED)`?\b')) {
            Add-SpecError $relative 'DoD содержит FAIL или BLOCKED evidence.'
        }
    }

    if ($relative -match '^docs/specs/accepted/' -and $status -ne 'accepted') {
        Add-SpecError $relative 'файл в accepted/ должен иметь status: accepted.'
    }
    if ($relative -match '^docs/specs/superseded/' -and $status -ne 'superseded') {
        Add-SpecError $relative 'файл в superseded/ должен иметь status: superseded.'
    }
}

if ($errors.Count -gt 0) {
    $errors | Sort-Object -Unique | ForEach-Object { Write-Error $_ -ErrorAction Continue }
    exit 1
}

Write-Host ("Spec contract passed: files={0}, phase={1}." -f @($files).Count, $Phase)
exit 0
