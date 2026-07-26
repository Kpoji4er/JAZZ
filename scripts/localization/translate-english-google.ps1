[CmdletBinding()]
param(
    [string] $CatalogPath,

    [string] $EnglishManualCsv,

    [ValidateRange(1000, 4500)]
    [int] $BatchCharacters = 4000,

    [ValidateRange(0, 5000)]
    [int] $DelayMilliseconds = 350,

    [switch] $AllowExternalTranslation
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

if (-not $AllowExternalTranslation) {
    throw "External translation is disabled. Pass -AllowExternalTranslation only after the project owner explicitly consents to sending mod-only text to Google Translate."
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [IO.Path]::GetFullPath((Join-Path $scriptRoot "..\.."))
if (-not $CatalogPath) {
    $CatalogPath = Join-Path $repoRoot "Localization\Strings.csv"
}
if (-not $EnglishManualCsv) {
    $EnglishManualCsv = Join-Path $repoRoot "Localization\EnglishManual.csv"
}

function Protect-TranslationTokens {
    param(
        [string] $SourceText,
        [int] $RowIndex
    )

    $pattern = [regex]::new(
        '(?s)(?:\\[nrt]|[\r\n\t]+|\{[^{}\r\n]+\}|%(?:[-+0-9.#]*[A-Za-z]|[A-Za-z_][A-Za-z0-9_]*))+'
    )
    $matches = @($pattern.Matches($SourceText))
    $tokens = [ordered]@{}
    $builder = New-Object Text.StringBuilder
    $position = 0
    for ($index = 0; $index -lt $matches.Count; $index++) {
        $match = $matches[$index]
        [void] $builder.Append($SourceText.Substring($position, $match.Index - $position))
        $marker = if ($match.Value -match '^[\r\n\t]+$') {
            '<br id="JZR{0:D6}T{1:D4}">' -f $RowIndex, $index
        }
        else {
            '<xjztoken id="R{0:D6}T{1:D4}"/>' -f $RowIndex, $index
        }
        $tokens[$marker] = $match.Value
        [void] $builder.Append($marker)
        $position = $match.Index + $match.Length
    }
    [void] $builder.Append($SourceText.Substring($position))
    return [pscustomobject]@{
        Text   = $builder.ToString()
        Tokens = $tokens
    }
}

function Restore-TranslationTokens {
    param(
        [string] $TranslatedText,
        [string] $SourceText,
        [System.Collections.IDictionary] $Tokens
    )

    $result = $TranslatedText.Trim()
    foreach ($marker in $Tokens.Keys) {
        if (-not $result.Contains($marker)) {
            throw "Google response lost protected token $marker."
        }
        $result = $result.Replace($marker, [string]$Tokens[$marker])
    }
    if ($result -match '<xjztoken\b') {
        throw "Google response contains an unknown protected token."
    }

    $sourceTags = @([regex]::Matches($SourceText, '<[^>]+>'))
    $translatedTags = @([regex]::Matches($result, '<[^>]+>'))
    if ($sourceTags.Count -ne $translatedTags.Count) {
        throw "Google response changed the number of angle tags: expected $($sourceTags.Count), got $($translatedTags.Count)."
    }
    for ($index = $translatedTags.Count - 1; $index -ge 0; $index--) {
        $match = $translatedTags[$index]
        $result = $result.Substring(0, $match.Index) +
            $sourceTags[$index].Value +
            $result.Substring($match.Index + $match.Length)
    }

    $sourceBreaks = @([regex]::Matches($SourceText, '\r\n|\r|\n|\t'))
    $translatedBreaks = @([regex]::Matches($result, '\r\n|\r|\n|\t'))
    if ($sourceBreaks.Count -ne $translatedBreaks.Count) {
        throw "Google response changed the number of line breaks: expected $($sourceBreaks.Count), got $($translatedBreaks.Count)."
    }
    for ($index = $translatedBreaks.Count - 1; $index -ge 0; $index--) {
        $match = $translatedBreaks[$index]
        $result = $result.Substring(0, $match.Index) +
            $sourceBreaks[$index].Value +
            $result.Substring($match.Index + $match.Length)
    }

    return $result
}

function Invoke-GoogleTranslation {
    param([string] $Payload)

    $endpoint = "https://translate.googleapis.com/translate_a/single"
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        try {
            $response = Invoke-RestMethod `
                -Uri $endpoint `
                -Method Post `
                -Body @{
                    client = "gtx"
                    sl     = "ru"
                    tl     = "en"
                    dt     = "t"
                    q      = $Payload
                } `
                -ContentType "application/x-www-form-urlencoded; charset=UTF-8" `
                -TimeoutSec 60
            return (($response[0] | ForEach-Object { $_[0] }) -join "")
        }
        catch {
            if ($attempt -eq 5) {
                throw
            }
            Start-Sleep -Seconds ([Math]::Min(8, [Math]::Pow(2, $attempt)))
        }
    }
}

function Write-EnglishManual {
    param([object[]] $Rows)

    $sorted = @($Rows | Sort-Object { [decimal]$_.AnchorID })
    for ($index = 0; $index -lt $sorted.Count; $index++) {
        $sorted[$index].N = [string]($index + 1)
    }
    $csv = @(
        $sorted |
            Select-Object N, AnchorID, SourceText, English, Notes |
            ConvertTo-Csv -NoTypeInformation
    )
    [IO.File]::WriteAllLines(
        [IO.Path]::GetFullPath($EnglishManualCsv),
        $csv,
        [Text.UTF8Encoding]::new($false)
    )
}

if (-not (Test-Path -LiteralPath $CatalogPath -PathType Leaf)) {
    throw "Catalog not found: $CatalogPath"
}

$catalog = @(Import-Csv -LiteralPath $CatalogPath -Encoding UTF8)
$manualRows = New-Object "System.Collections.Generic.List[object]"
$manualBySource = @{}
if (Test-Path -LiteralPath $EnglishManualCsv -PathType Leaf) {
    foreach ($row in Import-Csv -LiteralPath $EnglishManualCsv -Encoding UTF8) {
        if ($manualBySource.ContainsKey($row.SourceText)) {
            if ($manualBySource[$row.SourceText].English -ne $row.English) {
                throw "Conflicting EnglishManual.csv rows for source anchored at ID $($row.AnchorID)."
            }
            continue
        }
        $manualRows.Add($row)
        $manualBySource[$row.SourceText] = $row
    }
}

$pending = New-Object "System.Collections.Generic.List[object]"
$groups = @(
    $catalog |
        Where-Object { $_.Status -match 'needs-english' } |
        Group-Object SourceText
)
$rowIndex = 0
foreach ($group in $groups) {
    if ($manualBySource.ContainsKey($group.Name)) {
        continue
    }
    $anchorId = @($group.Group.ID | Sort-Object { [decimal]$_ })[0]
    $protected = Protect-TranslationTokens -SourceText $group.Name -RowIndex $rowIndex
    $pending.Add([pscustomobject]@{
        RowIndex  = $rowIndex
        AnchorID  = $anchorId
        SourceText = [string]$group.Name
        Protected = $protected.Text
        Tokens    = $protected.Tokens
    })
    $rowIndex++
}

if ($pending.Count -eq 0) {
    Write-Output "No untranslated unique source strings remain."
    exit 0
}

$batches = New-Object "System.Collections.Generic.List[object]"
$current = New-Object "System.Collections.Generic.List[object]"
$currentLength = 0
foreach ($entry in $pending) {
    $marker = "[[[JAZZROW{0:D6}]]]" -f $entry.RowIndex
    $payloadPart = "$marker`n$($entry.Protected)"
    $extraLength = $payloadPart.Length + $(if ($current.Count -gt 0) { 1 } else { 0 })
    if ($current.Count -gt 0 -and $currentLength + $extraLength -gt $BatchCharacters) {
        $batches.Add($current.ToArray())
        $current = New-Object "System.Collections.Generic.List[object]"
        $currentLength = 0
    }
    $current.Add($entry)
    $currentLength += $extraLength
}
if ($current.Count -gt 0) {
    $batches.Add($current.ToArray())
}

$translatedCount = 0
$batchNumber = 0
foreach ($batch in $batches) {
    $batchNumber++
    $parts = foreach ($entry in $batch) {
        "[[[JAZZROW{0:D6}]]]`n{1}" -f $entry.RowIndex, $entry.Protected
    }
    $responseText = Invoke-GoogleTranslation -Payload ($parts -join "`n")
    $matches = @(
        [regex]::Matches(
            $responseText,
            '(?ms)^\[\[\[JAZZROW(?<index>\d{6})\]\]\][ \t]*\r?\n(?<text>.*?)(?=^\[\[\[JAZZROW\d{6}\]\]\]|\z)'
        )
    )
    if ($matches.Count -ne $batch.Count) {
        throw "Google response row count mismatch in batch ${batchNumber}: expected $($batch.Count), got $($matches.Count)."
    }

    $entriesByIndex = @{}
    foreach ($entry in $batch) {
        $entriesByIndex[[string]$entry.RowIndex] = $entry
    }
    foreach ($match in $matches) {
        $index = [string][int]$match.Groups["index"].Value
        if (-not $entriesByIndex.ContainsKey($index)) {
            throw "Google response returned unexpected row marker $index."
        }
        $entry = $entriesByIndex[$index]
        $english = Restore-TranslationTokens `
            -TranslatedText $match.Groups["text"].Value `
            -SourceText $entry.SourceText `
            -Tokens $entry.Tokens
        $row = [pscustomobject]@{
            N          = ""
            AnchorID   = [string]$entry.AnchorID
            SourceText = [string]$entry.SourceText
            English    = $english
            Notes      = "google-draft"
        }
        $manualRows.Add($row)
        $manualBySource[$row.SourceText] = $row
        $translatedCount++
    }

    Write-EnglishManual -Rows $manualRows.ToArray()
    Write-Output "Progress: translated=$translatedCount/$($pending.Count); batch=$batchNumber/$($batches.Count)"
    if ($DelayMilliseconds -gt 0) {
        Start-Sleep -Milliseconds $DelayMilliseconds
    }
}

Write-Output "Google draft complete: translated=$translatedCount; unique pending=$($pending.Count)."
