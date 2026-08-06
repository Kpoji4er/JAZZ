[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $GameCsv,

    [string] $RussianCsv,

    [string] $EnglishCsv,

    [string] $RussianManualCsv,

    [string] $EnglishManualCsv,

    [string] $CatalogPath,

    [string] $CollisionPath,

    [switch] $UpdateCatalog,

    [string] $ExportRussianCsv,

    [string] $ExportEnglishCsv,

    [switch] $Strict
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [IO.Path]::GetFullPath((Join-Path $scriptRoot "..\.."))
$modsRoot = Split-Path -Parent $repoRoot

if (-not $RussianCsv) {
    $RussianCsv = Join-Path $repoRoot "Russian.csv"
}
if (-not $EnglishCsv) {
    $EnglishCsv = Join-Path $repoRoot "English.csv"
}
if (-not $RussianManualCsv) {
    $RussianManualCsv = Join-Path $repoRoot "Localization\RussianManual.csv"
}
if (-not $EnglishManualCsv) {
    $EnglishManualCsv = Join-Path $repoRoot "Localization\EnglishManual.csv"
}

if (-not $CatalogPath) {
    $CatalogPath = Join-Path $repoRoot "Localization\Strings.csv"
}
if (-not $CollisionPath) {
    $CollisionPath = Join-Path $repoRoot "Localization\Collisions.csv"
}

function Resolve-PackageRoot {
    param([string[]] $Names)

    foreach ($name in $Names) {
        $candidate = Join-Path $modsRoot $name
        if (Test-Path -LiteralPath $candidate -PathType Container) {
            return [IO.Path]::GetFullPath($candidate)
        }
    }
    return $null
}

$packageRoots = [ordered]@{
    "jazz"        = $repoRoot
    "jazz_assets" = Resolve-PackageRoot -Names @("jazz_assets", "jazz-assets", "Jazz Assets", "jazz assets")
    "jazz-maps"   = Resolve-PackageRoot -Names @("jazz-maps", "JAZZ Maps", "jazz maps")
    "jazz-units"  = Resolve-PackageRoot -Names @("jazz-units", "JAZZ Units", "jazz units")
}

foreach ($entry in $packageRoots.GetEnumerator()) {
    if (-not $entry.Value) {
        throw "Package '$($entry.Key)' was not found next to '$repoRoot'."
    }
}

if (-not (Test-Path -LiteralPath $GameCsv -PathType Leaf)) {
    throw "Base localization table not found: $GameCsv"
}
if (-not (Test-Path -LiteralPath $RussianCsv -PathType Leaf)) {
    throw "Priority Russian table not found: $RussianCsv"
}
if (-not (Test-Path -LiteralPath $EnglishCsv -PathType Leaf)) {
    throw "Current English table not found: $EnglishCsv"
}

Add-Type -AssemblyName Microsoft.VisualBasic

function Read-LocalizationCsv {
    param([string] $Path)

    $fullPath = [IO.Path]::GetFullPath($Path)
    $parser = New-Object Microsoft.VisualBasic.FileIO.TextFieldParser(
        $fullPath,
        [Text.Encoding]::UTF8,
        $true
    )
    $parser.TextFieldType = [Microsoft.VisualBasic.FileIO.FieldType]::Delimited
    $parser.SetDelimiters(",")
    $parser.HasFieldsEnclosedInQuotes = $true
    $parser.TrimWhiteSpace = $false

    $rows = New-Object "System.Collections.Generic.List[object]"
    $parseErrors = New-Object "System.Collections.Generic.List[string]"
    $hadSeparatorHint = $false
    $header = @()
    $wideRows = 0
    $recoveredRows = 0

    try {
        if (-not $parser.EndOfData) {
            $first = @($parser.ReadFields())
            $isSeparatorHint = (
                $first.Count -eq 1 -and $first[0].TrimStart([char]0xfeff) -eq "sep=,"
            ) -or (
                $first.Count -eq 2 -and
                $first[0].TrimStart([char]0xfeff) -eq "sep=" -and
                $first[1] -eq ""
            )
            if ($isSeparatorHint) {
                $hadSeparatorHint = $true
                if (-not $parser.EndOfData) {
                    $header = @($parser.ReadFields())
                }
            }
            else {
                $header = $first
            }
        }

        if ($header.Count -gt 0) {
            $header[0] = $header[0].TrimStart([char]0xfeff)
        }

        while (-not $parser.EndOfData) {
            try {
                $fields = @($parser.ReadFields())
            }
            catch {
                $errorLine = $parser.ErrorLine
                $fallback = [regex]::Match(
                    $errorLine,
                    '^(?<id>\d+),(?<text>[^,]*),(?<translation>.*),,,OK,,,,,(?<context>[^,]*),'
                )
                if ($fallback.Success) {
                    $rows.Add([pscustomobject]@{
                        ID          = $fallback.Groups["id"].Value
                        Text        = $fallback.Groups["text"].Value
                        Translation = $fallback.Groups["translation"].Value.Trim('"')
                        Context     = $fallback.Groups["context"].Value
                        Status      = "OK"
                        FieldCount  = 20
                    })
                    $wideRows++
                    $recoveredRows++
                    continue
                }

                $parseErrors.Add("line $($parser.ErrorLineNumber): $($_.Exception.Message)")
                continue
            }

            if ($fields.Count -eq 0 -or [string]::IsNullOrWhiteSpace($fields[0])) {
                continue
            }
            if ($fields[0] -notmatch '^\d+$') {
                $parseErrors.Add("line $($parser.LineNumber): non-numeric ID '$($fields[0])'")
                continue
            }
            if ($fields.Count -gt $header.Count) {
                $wideRows++
            }

            $contextIndex = if ($fields.Count -ge 11) { 10 } elseif ($fields.Count -ge 5) { 4 } else { -1 }
            $statusIndex = if ($fields.Count -ge 6) { 5 } else { -1 }
            $rows.Add([pscustomobject]@{
                ID          = $fields[0]
                Text        = if ($fields.Count -ge 2) { $fields[1] } else { "" }
                Translation = if ($fields.Count -ge 3) { $fields[2] } else { "" }
                Context     = if ($contextIndex -ge 0) { $fields[$contextIndex] } else { "" }
                Status      = if ($statusIndex -ge 0) { $fields[$statusIndex] } else { "" }
                FieldCount  = $fields.Count
            })
        }

        if ($wideRows -gt 0 -or $parseErrors.Count -gt 0) {
            $seenIds = @{}
            foreach ($row in $rows) {
                $seenIds[$row.ID] = $true
            }
            $rawCsv = [IO.File]::ReadAllText($fullPath, [Text.Encoding]::UTF8)
            $recordPattern = [regex]::new('(?ms)^(?<record>\d+,.*?)(?=^\d+,|\z)')
            foreach ($recordMatch in $recordPattern.Matches($rawCsv)) {
                $recordText = $recordMatch.Groups["record"].Value.TrimEnd()
                $idMatch = [regex]::Match($recordText, '^(?<id>\d+),')
                if (-not $idMatch.Success -or $seenIds.ContainsKey($idMatch.Groups["id"].Value)) {
                    continue
                }

                $reader = New-Object IO.StringReader($recordText)
                $recordParser = New-Object Microsoft.VisualBasic.FileIO.TextFieldParser($reader)
                try {
                    $recordParser.TextFieldType = [Microsoft.VisualBasic.FileIO.FieldType]::Delimited
                    $recordParser.SetDelimiters(",")
                    $recordParser.HasFieldsEnclosedInQuotes = $true
                    $recordParser.TrimWhiteSpace = $false
                    $recordFields = @($recordParser.ReadFields())
                    if ($recordFields.Count -ge 3 -and $recordFields[0] -match '^\d+$') {
                        $recordContextIndex = if ($recordFields.Count -ge 11) { 10 } elseif ($recordFields.Count -ge 5) { 4 } else { -1 }
                        $recordStatusIndex = if ($recordFields.Count -ge 6) { 5 } else { -1 }
                        $rows.Add([pscustomobject]@{
                            ID          = $recordFields[0]
                            Text        = $recordFields[1]
                            Translation = $recordFields[2]
                            Context     = if ($recordContextIndex -ge 0) { $recordFields[$recordContextIndex] } else { "" }
                            Status      = if ($recordStatusIndex -ge 0) { $recordFields[$recordStatusIndex] } else { "" }
                            FieldCount  = $recordFields.Count
                        })
                        $seenIds[$recordFields[0]] = $true
                        if ($recordFields.Count -gt $header.Count) {
                            $wideRows++
                        }
                        $recoveredRows++
                    }
                }
                catch {
                    $fallback = [regex]::Match(
                        $recordText,
                        '^(?<id>\d+),(?<text>[^,]*),(?<translation>.*),,,OK,,,,,(?<context>[^,]*),'
                    )
                    if ($fallback.Success) {
                        $rows.Add([pscustomobject]@{
                            ID          = $fallback.Groups["id"].Value
                            Text        = $fallback.Groups["text"].Value
                            Translation = $fallback.Groups["translation"].Value.Trim('"')
                            Context     = $fallback.Groups["context"].Value
                            Status      = "OK"
                            FieldCount  = 20
                        })
                        $seenIds[$fallback.Groups["id"].Value] = $true
                        $wideRows++
                        $recoveredRows++
                    }
                }
                finally {
                    $recordParser.Close()
                    $reader.Close()
                }
            }
        }
    }
    finally {
        $parser.Close()
    }

    return [pscustomobject]@{
        Path             = [IO.Path]::GetFullPath($Path)
        Header           = $header
        Rows             = $rows
        HadSeparatorHint = $hadSeparatorHint
        WideRows         = $wideRows
        RecoveredRows    = $recoveredRows
        ParseErrors      = $parseErrors
    }
}

function Group-RowsById {
    param([System.Collections.IEnumerable] $Rows)

    $result = @{}
    foreach ($row in $Rows) {
        if (-not $result.ContainsKey($row.ID)) {
            $result[$row.ID] = New-Object "System.Collections.Generic.List[object]"
        }
        $result[$row.ID].Add($row)
    }
    return $result
}

function ConvertFrom-LuaQuotedText {
    param([string] $Text)

    $builder = New-Object Text.StringBuilder
    for ($index = 0; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]
        if ($character -ne "\" -or $index + 1 -ge $Text.Length) {
            [void] $builder.Append($character)
            continue
        }

        $index++
        $escaped = $Text[$index]
        switch ($escaped) {
            "n" { [void] $builder.Append("`n") }
            "r" { [void] $builder.Append("`r") }
            "t" { [void] $builder.Append("`t") }
            "a" { [void] $builder.Append([char]7) }
            "b" { [void] $builder.Append([char]8) }
            "f" { [void] $builder.Append([char]12) }
            "v" { [void] $builder.Append([char]11) }
            "\" { [void] $builder.Append("\") }
            '"' { [void] $builder.Append('"') }
            "'" { [void] $builder.Append("'") }
            default {
                [void] $builder.Append("\")
                [void] $builder.Append($escaped)
            }
        }
    }
    return $builder.ToString()
}

function Get-LuaFilesWithoutMaps {
    param(
        [string] $PackageName,
        [string] $PackageRoot
    )

    $files = New-Object "System.Collections.Generic.List[object]"
    foreach ($file in Get-ChildItem -LiteralPath $PackageRoot -File -Filter "*.lua") {
        $files.Add($file)
    }
    $excludedTopDirectories = @(
        ".git",
        ".agents",
        ".codex",
        "codex_worktrees",
        "docs"
    )
    foreach ($directory in Get-ChildItem -LiteralPath $PackageRoot -Directory) {
        if ($directory.Name -in $excludedTopDirectories) {
            continue
        }
        if ($PackageName -eq "jazz-maps" -and $directory.Name -eq "Maps") {
            continue
        }
        foreach ($file in Get-ChildItem -LiteralPath $directory.FullName -Recurse -File -Filter "*.lua") {
            $files.Add($file)
        }
    }
    return $files
}

$tCallPattern = [regex]::new(
    '\bT\s*(?:\(\s*\{\s*|\(\s*|\{\s*)(?<id>\d{6,})\s*,\s*(?:--\[\[.*?\]\]\s*)*(?:"(?<double>(?:\\.|[^"\\])*)"|''(?<single>(?:\\.|[^''\\])*)'')'
)

function Read-LuaLocalizationUses {
    $uses = New-Object "System.Collections.Generic.List[object]"
    $unsupported = New-Object "System.Collections.Generic.List[string]"

    foreach ($package in $packageRoots.GetEnumerator()) {
        $metadataPath = Join-Path $package.Value "metadata.lua"
        $metadata = Get-Content -Raw -Encoding utf8 -LiteralPath $metadataPath

        foreach ($file in Get-LuaFilesWithoutMaps -PackageName $package.Key -PackageRoot $package.Value) {
            $relative = $file.FullName.Substring($package.Value.Length + 1)
            $relativeForward = $relative.Replace("\", "/")
            $state = "dormant"

            if ($relativeForward -eq "items.lua") {
                $state = "moditems"
            }
            elseif (
                $metadata.Contains('"' + $relativeForward + '"') -or
                $metadata.Contains("'" + $relativeForward + "'")
            ) {
                $state = "loaded"
            }

            $lines = [IO.File]::ReadAllLines($file.FullName, [Text.Encoding]::UTF8)
            for ($lineIndex = 0; $lineIndex -lt $lines.Length; $lineIndex++) {
                $lineNumber = $lineIndex + 1
                $line = $lines[$lineIndex]
                $scanText = $line

                if ($line -match '\bT\s*(?:\(|\{)\s*$') {
                    $lastLookahead = [Math]::Min($lineIndex + 4, $lines.Length - 1)
                    for ($lookahead = $lineIndex + 1; $lookahead -le $lastLookahead; $lookahead++) {
                        $scanText += "`n" + $lines[$lookahead]
                    }
                }

                foreach ($match in $tCallPattern.Matches($scanText)) {
                    $matchLineStart = $scanText.LastIndexOf(
                        "`n",
                        [Math]::Max(0, $match.Index - 1)
                    ) + 1
                    $matchPrefix = $scanText.Substring(
                        $matchLineStart,
                        $match.Index - $matchLineStart
                    )
                    if ($matchPrefix.TrimStart().StartsWith(
                        "--",
                        [StringComparison]::Ordinal
                    )) {
                        continue
                    }
                    $rawText = if ($match.Groups["double"].Success) {
                        $match.Groups["double"].Value
                    }
                    else {
                        $match.Groups["single"].Value
                    }
                    $uses.Add([pscustomobject]@{
                        ID      = $match.Groups["id"].Value
                        Text    = ConvertFrom-LuaQuotedText -Text $rawText
                        Package = $package.Key
                        File    = $relativeForward
                        Line    = $lineNumber
                        State   = $state
                    })
                }

                if ($line -match '\bT\s*(?:\(|\{)\s*\d{6,}\s*,\s*\[\[') {
                    $unsupported.Add("$($package.Key):$relativeForward`:$lineNumber")
                }
            }
        }
    }

    return [pscustomobject]@{
        Uses        = $uses
        Unsupported = $unsupported
    }
}

function Group-UsesById {
    param([System.Collections.IEnumerable] $Uses)

    $result = @{}
    foreach ($use in $Uses) {
        if (-not $result.ContainsKey($use.ID)) {
            $result[$use.ID] = New-Object "System.Collections.Generic.List[object]"
        }
        $result[$use.ID].Add($use)
    }
    return $result
}

function Get-DistinctStrings {
    param(
        [System.Collections.IEnumerable] $Values,
        [string] $Property
    )

    $result = @(
        $Values |
            ForEach-Object { $_.$Property } |
            Sort-Object -Unique
    )
    return ,$result
}

function Test-ContainsCyrillic {
    param([string] $Text)
    return $Text -match '[\p{IsCyrillic}]'
}

function ConvertTo-LocalizationTextKey {
    param([AllowNull()] $Text)

    if ($null -eq $Text) {
        return ""
    }
    $value = [string] $Text
    return $value.Replace([string][char]13 + [char]10, [string][char]10).Replace([string][char]13, [string][char]10)
}

function Group-TranslationsByIdAndText {
    param([System.Collections.IEnumerable] $Rows)

    $result = @{}
    foreach ($row in $Rows) {
        if ([string]::IsNullOrEmpty($row.Translation)) {
            continue
        }

        $id = [string] $row.ID
        if (-not $result.ContainsKey($id)) {
            $result[$id] = @{}
        }

        # Preserve case and surrounding whitespace. The shared key helper only
        # normalizes CRLF/CR to LF so multiline runtime rows remain comparable.
        $textKey = ConvertTo-LocalizationTextKey $row.Text
        $result[$id][$textKey] = [string] $row.Translation
    }
    return $result
}

function Test-LocalizationTextEqual {
    param(
        [AllowNull()] $Left,
        [AllowNull()] $Right
    )

    $leftText = ConvertTo-LocalizationTextKey $Left
    $rightText = ConvertTo-LocalizationTextKey $Right
    return $leftText.Equals($rightText, [StringComparison]::Ordinal)
}
function Test-LocalizationTextIn {
    param(
        [AllowNull()] $Text,
        [System.Collections.IEnumerable] $Values
    )

    foreach ($value in $Values) {
        if (Test-LocalizationTextEqual -Left $Text -Right $value) {
            return $true
        }
    }
    return $false
}

function ConvertTo-CsvCell {
    param([AllowNull()] $Value)

    $text = if ($null -eq $Value) { "" } else { [string] $Value }
    if ($text -match '[,"\r\n]|^\s|\s$') {
        return '"' + $text.Replace('"', '""') + '"'
    }
    return $text
}

function Write-CsvUtf8 {
    param(
        [string] $Path,
        [string[]] $Columns,
        [System.Collections.IEnumerable] $Rows,
        [string[]] $Prefix = @()
    )

    $fullPath = [IO.Path]::GetFullPath($Path)
    $directory = Split-Path -Parent $fullPath
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
        [void] (New-Item -ItemType Directory -Path $directory)
    }

    $lines = New-Object "System.Collections.Generic.List[string]"
    foreach ($prefixLine in $Prefix) {
        $lines.Add($prefixLine)
    }
    $lines.Add(($Columns | ForEach-Object { ConvertTo-CsvCell $_ }) -join ",")
    foreach ($row in $Rows) {
        $values = foreach ($column in $Columns) {
            ConvertTo-CsvCell $row.$column
        }
        $lines.Add($values -join ",")
    }

    $encoding = New-Object Text.UTF8Encoding($true)
    [IO.File]::WriteAllLines($fullPath, $lines, $encoding)
}

function Read-ExistingCatalog {
    param([string] $Path)

    $result = @{}
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $result
    }

    foreach ($row in Import-Csv -LiteralPath $Path -Encoding UTF8) {
        if ($row.ID -match '^\d+$') {
            $result[$row.ID] = $row
        }
    }
    return $result
}

$baseTable = Read-LocalizationCsv -Path $GameCsv
$russianTable = Read-LocalizationCsv -Path $RussianCsv
$englishTable = Read-LocalizationCsv -Path $EnglishCsv
$baseById = Group-RowsById -Rows $baseTable.Rows
$russianById = Group-RowsById -Rows $russianTable.Rows
$englishByIdAndText = Group-TranslationsByIdAndText -Rows $englishTable.Rows
$gameRussianCandidatesByText = @{}
foreach ($row in $baseTable.Rows) {
    $key = ConvertTo-LocalizationTextKey $row.Text
    if (-not $gameRussianCandidatesByText.ContainsKey($key)) {
        $gameRussianCandidatesByText[$key] = New-Object "System.Collections.Generic.List[string]"
    }
    if (-not [string]::IsNullOrEmpty($row.Translation)) {
        $gameRussianCandidatesByText[$key].Add([string] $row.Translation)
    }
}
$gameRussianByText = @{}
foreach ($key in $gameRussianCandidatesByText.Keys) {
    $variants = @($gameRussianCandidatesByText[$key] | Sort-Object -Unique)
    if ($variants.Count -eq 1) {
        $gameRussianByText[$key] = $variants[0]
    }
}

$gameEnglishCandidatesByText = @{}
foreach ($row in $baseTable.Rows) {
    if ([string]::IsNullOrEmpty($row.Translation) -or [string]::IsNullOrEmpty($row.Text)) {
        continue
    }
    $key = ConvertTo-LocalizationTextKey $row.Translation
    if (-not $gameEnglishCandidatesByText.ContainsKey($key)) {
        $gameEnglishCandidatesByText[$key] = New-Object "System.Collections.Generic.List[string]"
    }
    $gameEnglishCandidatesByText[$key].Add([string] $row.Text)
}
$gameEnglishByText = @{}
foreach ($key in $gameEnglishCandidatesByText.Keys) {
    $variants = @($gameEnglishCandidatesByText[$key] | Sort-Object -Unique)
    if ($variants.Count -eq 1) {
        $gameEnglishByText[$key] = $variants[0]
    }
}
$manualRussianByText = [System.Collections.Generic.Dictionary[string,string]]::new([System.StringComparer]::Ordinal)
$technicalRussianByText = [System.Collections.Generic.Dictionary[string,string]]::new([System.StringComparer]::Ordinal)
if (Test-Path -LiteralPath $RussianManualCsv -PathType Leaf) {
    foreach ($row in Import-Csv -LiteralPath $RussianManualCsv -Encoding UTF8) {
        if ([string]::IsNullOrEmpty($row.Russian)) {
            continue
        }
        $key = ConvertTo-LocalizationTextKey $row.SourceText
        $target = if ($row.Notes -eq "technical-copy") {
            $technicalRussianByText
        }
        else {
            $manualRussianByText
        }
        if ($target.ContainsKey($key) -and $target[$key] -ne $row.Russian) {
            throw "Conflicting RussianManual.csv translations for source text anchored at ID $($row.AnchorID)."
        }
        $target[$key] = [string] $row.Russian
    }
}

$manualEnglishByText = [System.Collections.Generic.Dictionary[string,string]]::new([System.StringComparer]::Ordinal)
$technicalEnglishByText = [System.Collections.Generic.Dictionary[string,string]]::new([System.StringComparer]::Ordinal)
if (Test-Path -LiteralPath $EnglishManualCsv -PathType Leaf) {
    foreach ($row in Import-Csv -LiteralPath $EnglishManualCsv -Encoding UTF8) {
        if ([string]::IsNullOrEmpty($row.English)) {
            continue
        }
        $key = ConvertTo-LocalizationTextKey $row.SourceText
        $target = if ($row.Notes -eq "technical-copy") {
            $technicalEnglishByText
        }
        else {
            $manualEnglishByText
        }
        if ($target.ContainsKey($key) -and $target[$key] -ne $row.English) {
            throw "Conflicting EnglishManual.csv translations for source text anchored at ID $($row.AnchorID)."
        }
        $target[$key] = [string] $row.English
    }
}
$luaScan = Read-LuaLocalizationUses


$activeUses = @($luaScan.Uses | Where-Object { $_.State -in @("loaded", "moditems") })
$dormantUses = @($luaScan.Uses | Where-Object { $_.State -eq "dormant" })
$activeById = Group-UsesById -Uses $activeUses
$dormantById = Group-UsesById -Uses $dormantUses

$collisionRows = New-Object "System.Collections.Generic.List[object]"
$blockingIds = @{}

foreach ($id in $activeById.Keys) {
    $uses = $activeById[$id]
    $texts = Get-DistinctStrings -Values $uses -Property "Text"
    if ($texts.Count -gt 1) {
        $blockingIds[$id] = $true
        foreach ($text in $texts) {
            $locations = @(
                $uses |
                    Where-Object Text -eq $text |
                    Sort-Object Package, File, Line |
                    ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
            ) -join " | "
            $collisionRows.Add([pscustomobject]@{
                ID            = $id
                Kind          = "active-id-collision"
                Text          = $text
                ReferenceText = ""
                Locations     = $locations
            })
        }
    }

    if ($baseById.ContainsKey($id)) {
        $baseTexts = Get-DistinctStrings -Values $baseById[$id] -Property "Text"
        foreach ($text in $texts) {
            if (-not (Test-LocalizationTextIn -Text $text -Values $baseTexts)) {
                $blockingIds[$id] = $true
                $collisionRows.Add([pscustomobject]@{
                    ID            = $id
                    Kind          = "game-id-collision"
                    Text          = $text
                    ReferenceText = $baseTexts -join " | "
                    Locations     = @(
                        $uses |
                            Where-Object Text -eq $text |
                            Sort-Object Package, File, Line |
                            ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
                    ) -join " | "
                })
            }
        }
    }
}

foreach ($id in $russianById.Keys) {
    $rows = $russianById[$id]
    $variants = @(
        $rows |
            ForEach-Object { "$($_.Text)$([char]31)$($_.Translation)" } |
            Sort-Object -Unique
    )
    if ($variants.Count -gt 1) {
        $blockingIds[$id] = $true
        foreach ($row in $rows) {
            $collisionRows.Add([pscustomobject]@{
                ID            = $id
                Kind          = "russian-csv-collision"
                Text          = $row.Text
                ReferenceText = $row.Translation
                Locations     = "Russian.csv"
            })
        }
    }
}

foreach ($id in $dormantById.Keys) {
    $uses = $dormantById[$id]
    $texts = Get-DistinctStrings -Values $uses -Property "Text"
    if ($texts.Count -gt 1) {
        foreach ($text in $texts) {
            $collisionRows.Add([pscustomobject]@{
                ID            = $id
                Kind          = "dormant-id-collision"
                Text          = $text
                ReferenceText = ""
                Locations     = @(
                    $uses |
                        Where-Object Text -eq $text |
                        Sort-Object Package, File, Line |
                        ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
                ) -join " | "
            })
        }
    }

    if ($activeById.ContainsKey($id)) {
        $activeTexts = Get-DistinctStrings -Values $activeById[$id] -Property "Text"
        foreach ($text in $texts) {
            if ($text -notin $activeTexts) {
                $collisionRows.Add([pscustomobject]@{
                    ID            = $id
                    Kind          = "dormant-vs-active"
                    Text          = $text
                    ReferenceText = $activeTexts -join " | "
                    Locations     = @(
                        $uses |
                            Where-Object Text -eq $text |
                            Sort-Object Package, File, Line |
                            ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
                    ) -join " | "
                })
            }
        }
    }
}

$catalogIds = @{}
foreach ($id in $russianById.Keys) {
    $catalogIds[$id] = $true
}
foreach ($id in $activeById.Keys) {
    $texts = Get-DistinctStrings -Values $activeById[$id] -Property "Text"
    $baseTexts = if ($baseById.ContainsKey($id)) {
        Get-DistinctStrings -Values $baseById[$id] -Property "Text"
    }
    else {
        @()
    }

    $isRelevant = (
        -not $baseById.ContainsKey($id) -or
        $texts.Count -gt 1 -or
        @($texts | Where-Object { $_ -notin $baseTexts }).Count -gt 0 -or
        @($texts | Where-Object { Test-ContainsCyrillic $_ }).Count -gt 0
    )
    if ($isRelevant) {
        $catalogIds[$id] = $true
    }
}

$existingCatalog = Read-ExistingCatalog -Path $CatalogPath
$catalogRows = New-Object "System.Collections.Generic.List[object]"

foreach ($id in @($catalogIds.Keys | Sort-Object { [decimal] $_ })) {
    $uses = @()
    if ($activeById.ContainsKey($id)) {
        $uses = @($activeById[$id] | ForEach-Object { $_ })
    }
    $texts = Get-DistinctStrings -Values $uses -Property "Text"
    $baseRows = @()
    if ($baseById.ContainsKey($id)) {
        $baseRows = @($baseById[$id] | ForEach-Object { $_ })
    }
    $baseTexts = Get-DistinctStrings -Values $baseRows -Property "Text"
    $russianRows = @()
    if ($russianById.ContainsKey($id)) {
        $russianRows = @($russianById[$id] | ForEach-Object { $_ })
    }
    $priorityRussian = if ($russianRows.Count -gt 0) { $russianRows[-1] } else { $null }
    $old = if ($existingCatalog.ContainsKey($id)) { $existingCatalog[$id] } else { $null }

    $sourceText = if ($texts.Count -eq 1) {
        $texts[0]
    }
    elseif ($priorityRussian -and $priorityRussian.Text) {
        $priorityRussian.Text
    }
    elseif ($baseTexts.Count -gt 0) {
        $baseTexts[0]
    }
    else {
        ""
    }

    $russian = ""
    $russianKey = ConvertTo-LocalizationTextKey $sourceText
    if ($manualRussianByText.ContainsKey($russianKey)) {
        $russian = $manualRussianByText[$russianKey]
    }
    elseif ($priorityRussian -and $priorityRussian.Translation) {
        $russian = $priorityRussian.Translation
    }
    elseif ($null -ne $old -and -not [string]::IsNullOrEmpty($old.Russian)) {
        $russian = $old.Russian
    }
    elseif ([string]::IsNullOrWhiteSpace($sourceText)) {
        $russian = $sourceText
    }
    elseif (Test-ContainsCyrillic $sourceText) {
        $russian = $sourceText
    }
    elseif ($gameRussianByText.ContainsKey((ConvertTo-LocalizationTextKey $sourceText))) {
        $russian = $gameRussianByText[(ConvertTo-LocalizationTextKey $sourceText)]
    }
    elseif ($technicalRussianByText.ContainsKey((ConvertTo-LocalizationTextKey $sourceText))) {
        $russian = $technicalRussianByText[(ConvertTo-LocalizationTextKey $sourceText)]
    }
    elseif ($baseRows.Count -gt 0 -and (Test-LocalizationTextIn -Text $sourceText -Values $baseTexts)) {
        $russian = $baseRows[-1].Translation
    }

    $english = ""
    $englishKey = ConvertTo-LocalizationTextKey $sourceText
    $currentEnglish = ""
    if (
        $englishByIdAndText.ContainsKey($id) -and
        $englishByIdAndText[$id].ContainsKey($englishKey)
    ) {
        $currentEnglish = $englishByIdAndText[$id][$englishKey]
    }
    if ($manualEnglishByText.ContainsKey($englishKey)) {
        $english = $manualEnglishByText[$englishKey]
    }
    elseif ($null -ne $old -and -not [string]::IsNullOrEmpty($old.English)) {
        $english = $old.English
    }
    elseif (-not [string]::IsNullOrEmpty($currentEnglish)) {
        $english = $currentEnglish
    }
    elseif ([string]::IsNullOrWhiteSpace($sourceText)) {
        $english = $sourceText
    }
    elseif ($texts.Count -le 1 -and $sourceText -and -not (Test-ContainsCyrillic $sourceText)) {
        $english = $sourceText
    }
    elseif ($gameEnglishByText.ContainsKey($englishKey)) {
        $english = $gameEnglishByText[$englishKey]
    }
    elseif ($technicalEnglishByText.ContainsKey($englishKey)) {
        $english = $technicalEnglishByText[$englishKey]
    }
    elseif ($baseTexts.Count -eq 1 -and (Test-LocalizationTextEqual -Left $sourceText -Right $baseTexts[0])) {
        $english = $baseTexts[0]
    }
    $statuses = New-Object "System.Collections.Generic.List[string]"
    if ($texts.Count -gt 1) {
        $statuses.Add("active-id-collision")
    }
    if ($baseTexts.Count -gt 0 -and @($texts | Where-Object { -not (Test-LocalizationTextIn -Text $_ -Values $baseTexts) }).Count -gt 0) {
        $statuses.Add("game-id-collision")
    }
    if ($russianRows.Count -gt 1) {
        $russianVariants = @(
            $russianRows |
                ForEach-Object { "$($_.Text)$([char]31)$($_.Translation)" } |
                Sort-Object -Unique
        )
        if ($russianVariants.Count -gt 1) {
            $statuses.Add("russian-csv-collision")
        }
    }
    if ($priorityRussian) {
        $statuses.Add("russian-override")
    }
    if ($baseRows.Count -eq 0) {
        $statuses.Add("new-id")
    }
    if ($uses.Count -eq 0) {
        $statuses.Add("unreferenced-russian-override")
    }
    if (-not $russian -and -not [string]::IsNullOrWhiteSpace($sourceText)) {
        $statuses.Add("needs-russian")
    }
    if (-not $english -and -not [string]::IsNullOrWhiteSpace($sourceText)) {
        $statuses.Add("needs-english")
    }
    if ($statuses.Count -eq 0) {
        $statuses.Add("ready")
    }

    $locations = @(
        $uses |
            Sort-Object Package, File, Line |
            ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
    ) -join " | "
    $packages = @($uses | ForEach-Object { $_.Package } | Sort-Object -Unique) -join " | "
    $context = if ($priorityRussian -and $priorityRussian.Context) {
        $priorityRussian.Context
    }
    elseif ($locations) {
        $locations
    }
    elseif ($baseRows.Count -gt 0) {
        $baseRows[-1].Context
    }
    else {
        ""
    }

    $catalogRows.Add([pscustomobject]@{
        ID          = $id
        SourceText  = $sourceText
        VanillaText = $baseTexts -join " | "
        Russian     = $russian
        English     = $english
        Status      = $statuses -join ";"
        Context     = $context
        Packages    = $packages
        Locations   = $locations
        Notes       = if ($null -ne $old) { $old.Notes } else { "" }
    })
}

Write-Verbose "Catalog rows prepared: $($catalogRows.Count)"

if ($UpdateCatalog) {
    Write-CsvUtf8 `
        -Path $CatalogPath `
        -Columns @("ID", "SourceText", "VanillaText", "Russian", "English", "Status", "Context", "Packages", "Locations", "Notes") `
        -Rows $catalogRows

    Write-Verbose "Catalog CSV written"

    Write-CsvUtf8 `
        -Path $CollisionPath `
        -Columns @("ID", "Kind", "Text", "ReferenceText", "Locations") `
        -Rows @($collisionRows | Sort-Object ID, Kind, Text)
}

function Export-EngineLocalizationTable {
    param(
        [string] $Language,
        [string] $Path
    )

    $translationProperty = if ($Language -eq "Russian") { "Russian" } else { "English" }
    $exportRows = @(
        $catalogRows |
            Where-Object {
                $activeById.ContainsKey([string]$_.ID) -and
                -not $baseById.ContainsKey([string]$_.ID)
            }
    )
    $incomplete = @(
        $exportRows |
            Where-Object {
                (-not $_.$translationProperty -and -not [string]::IsNullOrWhiteSpace($_.SourceText)) -or
                $_.Status -match 'collision'
            }
    )
    if ($incomplete.Count -gt 0) {
        throw "Cannot export $Language table: $($incomplete.Count) catalog row(s) are incomplete or colliding."
    }

    $engineRows = foreach ($row in $exportRows) {
        [pscustomobject]@{
            ID          = $row.ID
            Text        = $row.SourceText
            Translation = $row.$translationProperty
            VoiceActor  = ""
            Context     = $row.Context
        }
    }
    Write-CsvUtf8 `
        -Path $Path `
        -Columns @("ID", "Text", "Translation", "VoiceActor", "Context") `
        -Rows $engineRows `
        -Prefix @("sep=,")
}

if ($ExportRussianCsv) {
    Export-EngineLocalizationTable -Language "Russian" -Path $ExportRussianCsv
}
if ($ExportEnglishCsv) {
    Export-EngineLocalizationTable -Language "English" -Path $ExportEnglishCsv
}

$activeConflictIds = @{}
$gameConflictIds = @{}
$russianConflictIds = @{}
$dormantConflictIds = @{}
foreach ($collision in $collisionRows) {
    switch -Wildcard ($collision.Kind) {
        "active-id-collision" { $activeConflictIds[$collision.ID] = $true }
        "game-id-collision" { $gameConflictIds[$collision.ID] = $true }
        "russian-csv-collision" { $russianConflictIds[$collision.ID] = $true }
        "dormant*" { $dormantConflictIds[$collision.ID] = $true }
    }
}
$activeConflictCount = $activeConflictIds.Count
$gameConflictCount = $gameConflictIds.Count
$russianConflictCount = $russianConflictIds.Count
$dormantConflictCount = $dormantConflictIds.Count
$needsRussianCount = @($catalogRows | Where-Object Status -match 'needs-russian').Count
$needsEnglishCount = @($catalogRows | Where-Object Status -match 'needs-english').Count

Write-Output "JAZZ localization audit"
Write-Output "Base Game.csv rows: $($baseTable.Rows.Count); unique IDs: $($baseById.Count)"
Write-Output "Priority Russian.csv rows: $($russianTable.Rows.Count); unique IDs: $($russianById.Count)"
Write-Output "Current English.csv rows: $($englishTable.Rows.Count); source-aware IDs: $($englishByIdAndText.Count)"
Write-Output "Lua T uses: active=$($activeUses.Count), dormant=$($dormantUses.Count); active IDs=$($activeById.Count)"
Write-Output "Catalog rows: $($catalogRows.Count); needs Russian=$needsRussianCount; needs English=$needsEnglishCount"
Write-Output "Collisions: active=$activeConflictCount, against Game.csv=$gameConflictCount, Russian.csv=$russianConflictCount, dormant=$dormantConflictCount"

if ($russianTable.WideRows -gt 0) {
    Write-Warning "Russian.csv declares $($russianTable.Header.Count) columns but contains $($russianTable.WideRows) wider data row(s)."
}
if ($englishTable.WideRows -gt 0) {
    Write-Warning "English.csv declares $($englishTable.Header.Count) columns but contains $($englishTable.WideRows) wider data row(s)."
}
foreach ($errorText in $baseTable.ParseErrors) {
    Write-Warning "Game.csv: $errorText"
}
foreach ($errorText in $russianTable.ParseErrors) {
    Write-Warning "Russian.csv: $errorText"
}
foreach ($errorText in $englishTable.ParseErrors) {
    Write-Warning "English.csv: $errorText"
}
foreach ($location in $luaScan.Unsupported) {
    Write-Warning "Unsupported multiline/long-string T form near $location"
}
if ($UpdateCatalog) {
    Write-Output "Updated: $([IO.Path]::GetFullPath($CatalogPath))"
    Write-Output "Updated: $([IO.Path]::GetFullPath($CollisionPath))"
}

$hasBlockingIssues = (
    $blockingIds.Count -gt 0 -or
    $russianTable.WideRows -gt 0 -or
    $englishTable.WideRows -gt 0 -or
    $baseTable.ParseErrors.Count -gt 0 -or
    $russianTable.ParseErrors.Count -gt 0 -or
    $englishTable.ParseErrors.Count -gt 0 -or
    $luaScan.Unsupported.Count -gt 0
)
if ($Strict -and $hasBlockingIssues) {
    exit 2
}
