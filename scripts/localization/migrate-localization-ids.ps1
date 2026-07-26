[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $GameCsv,

    [string] $GameSourceRoot,

    [ValidateSet("Plan", "Apply")]
    [string] $Mode = "Plan",

    [string] $CatalogPath,

    [string] $ManifestPath,

    [string] $AmbiguityPath,

    [Int64] $RangeStart = 890000000000000,

    [Int64] $RangeEnd = 890000000099999
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [IO.Path]::GetFullPath((Join-Path $scriptRoot "..\.."))
$modsRoot = Split-Path -Parent $repoRoot

if (-not $CatalogPath) {
    $CatalogPath = Join-Path $repoRoot "Localization\Strings.csv"
}
if (-not $ManifestPath) {
    $ManifestPath = Join-Path $repoRoot "Localization\IdMigration.csv"
}
if (-not $AmbiguityPath) {
    $AmbiguityPath = Join-Path $repoRoot "Localization\IdAmbiguities.csv"
}

foreach ($requiredPath in @($GameCsv, $CatalogPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file does not exist: $requiredPath"
    }
}
if ($RangeStart -lt 1 -or $RangeEnd -lt $RangeStart) {
    throw "Invalid localization ID range: $RangeStart..$RangeEnd"
}
if ($RangeEnd -ge 9007199254740992) {
    throw "Localization ID range must stay below 2^53."
}

function Resolve-PackageRoot {
    param([string[]] $Names)

    foreach ($name in $Names) {
        $candidate = Join-Path $modsRoot $name
        if (Test-Path -LiteralPath $candidate -PathType Container) {
            return [IO.Path]::GetFullPath($candidate)
        }
    }
    throw "Cannot resolve package root from: $($Names -join ', ')"
}

$packageRoots = [ordered]@{
    "jazz"        = $repoRoot
    "jazz_assets" = Resolve-PackageRoot -Names @("jazz_assets", "jazz-assets")
    "jazz-maps"   = Resolve-PackageRoot -Names @("jazz-maps", "jazz_maps")
    "jazz-units"  = Resolve-PackageRoot -Names @("jazz-units", "jazz_units")
}

function ConvertTo-CsvCell {
    param([AllowNull()] $Value)

    $text = if ($null -eq $Value) { "" } else { [string]$Value }
    if ($text -match '[,"\r\n]' -or $text -ne $text.Trim()) {
        return '"' + $text.Replace('"', '""') + '"'
    }
    return $text
}

function Write-CsvUtf8 {
    param(
        [string] $Path,
        [string[]] $Columns,
        [System.Collections.IEnumerable] $Rows
    )

    $lines = New-Object "System.Collections.Generic.List[string]"
    $lines.Add(($Columns | ForEach-Object { ConvertTo-CsvCell $_ }) -join ",")
    foreach ($row in $Rows) {
        $lines.Add(($Columns | ForEach-Object { ConvertTo-CsvCell $row.$_ }) -join ",")
    }

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent -PathType Container)) {
        [void](New-Item -ItemType Directory -Path $parent)
    }
    [IO.File]::WriteAllLines(
        [IO.Path]::GetFullPath($Path),
        $lines,
        (New-Object Text.UTF8Encoding($false))
    )
}

function ConvertFrom-LuaQuotedText {
    param([string] $Text)

    $builder = New-Object Text.StringBuilder
    for ($index = 0; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]
        if ($character -ne "\" -or $index + 1 -ge $Text.Length) {
            [void]$builder.Append($character)
            continue
        }

        $index++
        $escaped = $Text[$index]
        switch ($escaped) {
            "n" { [void]$builder.Append("`n") }
            "r" { [void]$builder.Append("`r") }
            "t" { [void]$builder.Append("`t") }
            "a" { [void]$builder.Append([char]7) }
            "b" { [void]$builder.Append([char]8) }
            "f" { [void]$builder.Append([char]12) }
            "v" { [void]$builder.Append([char]11) }
            "\" { [void]$builder.Append("\") }
            '"' { [void]$builder.Append('"') }
            "'" { [void]$builder.Append("'") }
            default {
                [void]$builder.Append("\")
                [void]$builder.Append($escaped)
            }
        }
    }
    return $builder.ToString()
}

function ConvertTo-LuaQuotedText {
    param(
        [string] $Text,
        [string] $Quote
    )

    $result = $Text.Replace("\", "\\")
    $result = $result.Replace("`r`n", "\n").Replace("`r", "\n").Replace("`n", "\n")
    $result = $result.Replace("`t", "\t")
    if ($Quote -eq '"') {
        $result = $result.Replace('"', '\"')
    }
    else {
        $result = $result.Replace("'", "\'")
    }
    return $result
}

function Normalize-LocalizationText {
    param([string] $Text)
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n")
}

function Get-TextKey {
    param([string] $Text)

    $normalized = Normalize-LocalizationText -Text $Text
    return [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($normalized))
}

function Get-PairKey {
    param(
        [string] $ID,
        [string] $Text
    )
    return $ID + [char]31 + (Get-TextKey -Text $Text)
}

function Get-UseContextKey {
    param([object] $Use)

    if ([string]::IsNullOrWhiteSpace($Use.Comment)) {
        return ""
    }
    return Get-NormalizedGeneratedContext -Comment $Use.Comment
}

function Get-GroupKey {
    param(
        [string] $ID,
        [string] $Text,
        [string] $ContextKey
    )

    return (
        $ID +
        [char]31 +
        (Get-TextKey -Text $Text) +
        [char]31 +
        $ContextKey
    )
}

function Get-LuaFilesWithoutMaps {
    param(
        [string] $PackageName,
        [string] $PackageRoot
    )

    $excludedTopDirectories = @(
        ".git",
        ".agents",
        ".codex",
        "codex_worktrees",
        "docs"
    )
    $files = New-Object "System.Collections.Generic.List[IO.FileInfo]"
    foreach ($file in Get-ChildItem -LiteralPath $PackageRoot -File -Filter "*.lua") {
        $files.Add($file)
    }
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

function Read-Utf8File {
    param([string] $Path)

    $bytes = [IO.File]::ReadAllBytes($Path)
    $hasBom = (
        $bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF
    )
    $offset = if ($hasBom) { 3 } else { 0 }
    return [pscustomobject]@{
        Text   = [Text.Encoding]::UTF8.GetString($bytes, $offset, $bytes.Length - $offset)
        HasBom = $hasBom
    }
}

function Write-Utf8File {
    param(
        [string] $Path,
        [string] $Text,
        [bool] $HasBom
    )

    [IO.File]::WriteAllText(
        $Path,
        $Text,
        (New-Object Text.UTF8Encoding($HasBom))
    )
}

$tCallPattern = [regex]::new(
    '\bT\s*(?:\(\s*\{\s*|\(\s*|\{\s*)(?<id>\d{6,})\s*,\s*(?:--\[\[(?<comment>.*?)\]\]\s*)*(?:"(?<double>(?:\\.|[^"\\])*)"|''(?<single>(?:\\.|[^''\\])*)'')'
)

function Test-IsLineCommentedTCall {
    param(
        [string] $FileText,
        [Text.RegularExpressions.Match] $Match
    )

    $lineStart = $FileText.LastIndexOf("`n", [Math]::Max(0, $Match.Index - 1)) + 1
    $prefix = $FileText.Substring($lineStart, $Match.Index - $lineStart)
    return $prefix.TrimStart().StartsWith("--", [StringComparison]::Ordinal)
}

function Get-InferredGeneratedComment {
    param(
        [string] $FileText,
        [Text.RegularExpressions.Match] $Match
    )

    $lineStart = $FileText.LastIndexOf("`n", [Math]::Max(0, $Match.Index - 1)) + 1
    $prefix = $FileText.Substring($lineStart, $Match.Index - $lineStart)
    if ($prefix -notmatch "'display_name'\s*,\s*$") {
        return ""
    }

    $nextSector = $FileText.IndexOf(
        "PlaceObj('SatelliteSector'",
        $Match.Index + $Match.Length,
        [StringComparison]::Ordinal
    )
    $scanEnd = [Math]::Min($FileText.Length, $Match.Index + $Match.Length + 3000)
    if ($nextSector -ge 0) {
        $scanEnd = [Math]::Min($scanEnd, $nextSector)
    }
    $after = $FileText.Substring(
        $Match.Index + $Match.Length,
        $scanEnd - ($Match.Index + $Match.Length)
    )
    $imageMatch = [regex]::Match(
        $after,
        "'image'\s*,\s*[`"']UI/SatelliteView/SectorImages/(?<letters>[A-Z]+)(?<digits>\d+)[`"']"
    )
    if (-not $imageMatch.Success) {
        return ""
    }

    $sector = (
        $imageMatch.Groups["letters"].Value +
        ([int]$imageMatch.Groups["digits"].Value).ToString()
    )
    return "ModItemCampaignPreset HotDiamonds display_name Sector name for $sector"
}

function Read-LuaUses {
    $uses = New-Object "System.Collections.Generic.List[object]"

    foreach ($package in $packageRoots.GetEnumerator()) {
        $metadataPath = Join-Path $package.Value "metadata.lua"
        $metadata = [IO.File]::ReadAllText($metadataPath, [Text.Encoding]::UTF8)

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

            $fileData = Read-Utf8File -Path $file.FullName
            $line = 1
            $lastIndex = 0
            foreach ($match in $tCallPattern.Matches($fileData.Text)) {
                if ($match.Index -gt $lastIndex) {
                    $segment = $fileData.Text.Substring($lastIndex, $match.Index - $lastIndex)
                    $line += ([regex]::Matches($segment, "`n")).Count
                }
                $lastIndex = $match.Index

                if (Test-IsLineCommentedTCall -FileText $fileData.Text -Match $match) {
                    continue
                }

                $isDouble = $match.Groups["double"].Success
                $textGroup = if ($isDouble) {
                    $match.Groups["double"]
                }
                else {
                    $match.Groups["single"]
                }
                $comment = $match.Groups["comment"].Value
                if ([string]::IsNullOrWhiteSpace($comment)) {
                    $comment = Get-InferredGeneratedComment `
                        -FileText $fileData.Text `
                        -Match $match
                }
                $uses.Add([pscustomobject]@{
                    ID          = $match.Groups["id"].Value
                    Text        = ConvertFrom-LuaQuotedText -Text $textGroup.Value
                    Comment     = $comment
                    Quote       = if ($isDouble) { '"' } else { "'" }
                    Package     = $package.Key
                    PackageRoot = $package.Value
                    FullPath    = $file.FullName
                    File        = $relativeForward
                    Line        = $line
                    State       = $state
                    IDIndex     = $match.Groups["id"].Index
                    IDLength    = $match.Groups["id"].Length
                    TextIndex   = $textGroup.Index
                    TextLength  = $textGroup.Length
                    HasBom      = $fileData.HasBom
                })
            }
        }
    }
    return $uses
}

function Add-ToLookup {
    param(
        [hashtable] $Lookup,
        [string] $Text,
        [object] $Row
    )

    if ([string]::IsNullOrEmpty($Text)) {
        return
    }
    $key = Get-TextKey -Text $Text
    if (-not $Lookup.ContainsKey($key)) {
        $Lookup[$key] = New-Object "System.Collections.Generic.List[object]"
    }
    $Lookup[$key].Add($Row)
}

function Get-GameCandidates {
    param([string] $Text)

    $key = Get-TextKey -Text $Text
    $byId = @{}
    foreach ($lookup in @($gameByText, $gameByTranslation)) {
        if ($lookup.ContainsKey($key)) {
            foreach ($row in $lookup[$key]) {
                $byId[$row.ID] = $row
            }
        }
    }
    return @($byId.Values)
}

function Get-CommentOwnerTokens {
    param([System.Collections.IEnumerable] $Uses)

    $tokens = @{}
    foreach ($use in $Uses) {
        if ([string]::IsNullOrWhiteSpace($use.Comment)) {
            continue
        }
        $parts = @($use.Comment -split '\s+' | Where-Object { $_ })
        if ($parts.Count -ge 2) {
            $tokens[$parts[1]] = $true
        }
    }
    return @($tokens.Keys)
}

function Get-NormalizedGeneratedContext {
    param([string] $Comment)

    $context = $Comment.Trim()
    if ($context.StartsWith("ModItem", [StringComparison]::Ordinal)) {
        $context = $context.Substring(7)
    }
    return $context
}

function Select-GameCandidate {
    param(
        [string] $OldID,
        [string] $OldText,
        [System.Collections.IEnumerable] $Uses,
        [System.Collections.IEnumerable] $Candidates
    )

    $candidateRows = @($Candidates)
    if ($candidateRows.Count -eq 0) {
        return [pscustomobject]@{
            Row          = $null
            MatchKind    = ""
            Ambiguous    = $false
            CandidateIDs = ""
        }
    }

    $candidateIds = @($candidateRows.ID | Sort-Object { [decimal]$_ }) -join " | "
    $comments = @(
        $Uses |
            ForEach-Object { Get-NormalizedGeneratedContext -Comment $_.Comment } |
            Where-Object { $_ } |
            Sort-Object -Unique
    )

    if ($comments.Count -gt 0) {
        $ownerTokens = @(Get-CommentOwnerTokens -Uses $Uses)
        $scored = foreach ($row in $candidateRows) {
            $score = 0
            $gameContext = if ($row.Context) { $row.Context.Trim() } else { "" }
            foreach ($comment in $comments) {
                if ($gameContext -and $comment.Equals($gameContext, [StringComparison]::Ordinal)) {
                    $score = [Math]::Max($score, 100000)
                }
                elseif (
                    $gameContext -and
                    (
                        $comment.StartsWith($gameContext + " ", [StringComparison]::Ordinal) -or
                        $gameContext.StartsWith($comment + " ", [StringComparison]::Ordinal)
                    )
                ) {
                    $score = [Math]::Max(
                        $score,
                        50000 + [Math]::Min($comment.Length, $gameContext.Length)
                    )
                }
            }
            foreach ($token in $ownerTokens) {
                if ($row.Context -match ('[\\/]' + [regex]::Escape($token) + '(?:\.generated)?\.lua\(')) {
                    $score = [Math]::Max($score, 1000)
                }
            }
            [pscustomobject]@{
                Row   = $row
                Score = $score
            }
        }

        $maxScore = @($scored | Measure-Object Score -Maximum).Maximum
        $best = @($scored | Where-Object Score -eq $maxScore)
        if ($maxScore -gt 0 -and $best.Count -eq 1) {
            return [pscustomobject]@{
                Row          = $best[0].Row
                MatchKind    = "generated-context"
                Ambiguous    = $false
                CandidateIDs = $candidateIds
            }
        }
        if ($maxScore -gt 0) {
            $currentBest = @($best | Where-Object { $_.Row.ID -eq $OldID })
            if ($currentBest.Count -eq 1) {
                return [pscustomobject]@{
                    Row          = $currentBest[0].Row
                    MatchKind    = "generated-context-current-id"
                    Ambiguous    = $false
                    CandidateIDs = $candidateIds
                }
            }
            return [pscustomobject]@{
                Row          = $null
                MatchKind    = "ambiguous-generated-context"
                Ambiguous    = $true
                CandidateIDs = $candidateIds
            }
        }
        return [pscustomobject]@{
            Row          = $null
            MatchKind    = "generated-context-not-in-game"
            Ambiguous    = $false
            CandidateIDs = $candidateIds
        }
    }

    $current = @($candidateRows | Where-Object ID -eq $OldID)
    if ($current.Count -eq 1) {
        $kind = if (
            (Normalize-LocalizationText $OldText) -eq
            (Normalize-LocalizationText $current[0].Text)
        ) {
            "current-game-text"
        }
        else {
            "current-game-translation"
        }
        return [pscustomobject]@{
            Row          = $current[0]
            MatchKind    = $kind
            Ambiguous    = $false
            CandidateIDs = $candidateIds
        }
    }

    if ($candidateRows.Count -eq 1) {
        $row = $candidateRows[0]
        $kind = if (
            (Normalize-LocalizationText $OldText) -eq
            (Normalize-LocalizationText $row.Text)
        ) {
            "unique-game-text"
        }
        else {
            "unique-game-translation"
        }
        return [pscustomobject]@{
            Row          = $row
            MatchKind    = $kind
            Ambiguous    = $false
            CandidateIDs = $candidateIds
        }
    }

    $texts = @($candidateRows.Text | Sort-Object -Unique)
    $translations = @($candidateRows.Translation | Sort-Object -Unique)
    if ($texts.Count -eq 1 -and $translations.Count -eq 1) {
        $row = @($candidateRows | Sort-Object { [decimal]$_.ID })[0]
        return [pscustomobject]@{
            Row          = $row
            MatchKind    = "equivalent-game-rows"
            Ambiguous    = $false
            CandidateIDs = $candidateIds
        }
    }

    return [pscustomobject]@{
        Row          = $null
        MatchKind    = "ambiguous-game-match"
        Ambiguous    = $true
        CandidateIDs = $candidateIds
    }
}

function Get-AnalysisOrderKey {
    param([object] $Analysis)

    $use = @(
        $Analysis.Uses |
            Sort-Object `
                @{ Expression = { if ($_.File -eq "items.lua") { 0 } else { 1 } } }, `
                Package, `
                File, `
                Line
    )[0]
    $fileRank = if ($use.File -eq "items.lua") { "0" } else { "1" }
    return (
        $use.Package +
        [char]31 +
        $fileRank +
        [char]31 +
        $use.File +
        [char]31 +
        ([int]$use.Line).ToString("0000000000")
    )
}

function Get-GameSourceRelativePath {
    param([string] $Location)

    if ($Location -match '^Trunk[\\/]Zulu[\\/](?<relative>.+?)\(\d+\)$') {
        return $Matches["relative"].Replace("/", "\")
    }
    return ""
}

function Read-VanillaSourceUsesForAnalyses {
    param([System.Collections.IEnumerable] $Analyses)

    if ([string]::IsNullOrWhiteSpace($GameSourceRoot)) {
        return @()
    }
    if (-not (Test-Path -LiteralPath $GameSourceRoot -PathType Container)) {
        throw "Game source root does not exist: $GameSourceRoot"
    }

    $paths = @{}
    foreach ($analysis in $Analyses) {
        if (-not $analysis.Ambiguous -or -not $analysis.ContextKey) {
            continue
        }
        foreach ($candidate in @(Get-GameCandidates -Text $analysis.OldText)) {
            if (-not $candidate.Context) {
                continue
            }
            if (-not $candidate.Context.Trim().Equals(
                $analysis.ContextKey,
                [StringComparison]::Ordinal
            )) {
                continue
            }
            $relative = Get-GameSourceRelativePath -Location $candidate.Location
            if (-not $relative) {
                continue
            }
            $fullPath = [IO.Path]::GetFullPath((Join-Path $GameSourceRoot $relative))
            if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
                $paths[$fullPath] = $relative.Replace("\", "/")
            }
        }
    }

    $uses = New-Object "System.Collections.Generic.List[object]"
    foreach ($entry in $paths.GetEnumerator()) {
        $fileData = Read-Utf8File -Path $entry.Key
        $line = 1
        $lastIndex = 0
        foreach ($match in $tCallPattern.Matches($fileData.Text)) {
            if ($match.Index -gt $lastIndex) {
                $segment = $fileData.Text.Substring($lastIndex, $match.Index - $lastIndex)
                $line += ([regex]::Matches($segment, "`n")).Count
            }
            $lastIndex = $match.Index

            $isDouble = $match.Groups["double"].Success
            $textGroup = if ($isDouble) {
                $match.Groups["double"]
            }
            else {
                $match.Groups["single"]
            }
            $comment = $match.Groups["comment"].Value
            $uses.Add([pscustomobject]@{
                ID         = $match.Groups["id"].Value
                Text       = ConvertFrom-LuaQuotedText -Text $textGroup.Value
                ContextKey = if ($comment) {
                    Get-NormalizedGeneratedContext -Comment $comment
                }
                else {
                    ""
                }
                File       = $entry.Value
                Line       = $line
            })
        }
    }
    return $uses
}

function Test-VanillaUseTextMatch {
    param(
        [object] $VanillaUse,
        [object] $Analysis
    )

    $oldText = Normalize-LocalizationText -Text $Analysis.OldText
    if ($oldText -eq (Normalize-LocalizationText -Text $VanillaUse.Text)) {
        return $true
    }
    if ($gameById.ContainsKey($VanillaUse.ID)) {
        return $oldText -eq (
            Normalize-LocalizationText -Text $gameById[$VanillaUse.ID].Translation
        )
    }
    return $false
}

function Resolve-AmbiguitiesFromVanillaSource {
    param([System.Collections.IEnumerable] $Analyses)

    $analysisArray = @($Analyses | ForEach-Object { $_ })
    $vanillaUses = @(
        Read-VanillaSourceUsesForAnalyses -Analyses $analysisArray |
            ForEach-Object { $_ }
    )
    if ($vanillaUses.Count -eq 0) {
        return 0
    }

    $resolved = 0
    $buckets = @(
        $analysisArray |
            Where-Object { $_.ContextKey } |
            Group-Object {
                $_.ContextKey + [char]31 + (Get-TextKey -Text $_.OldText)
            }
    )
    foreach ($bucket in $buckets) {
        $modRows = @(
            $bucket.Group |
                Sort-Object { Get-AnalysisOrderKey -Analysis $_ }
        )
        if (@($modRows | Where-Object Ambiguous).Count -eq 0) {
            continue
        }

        $contextKey = $modRows[0].ContextKey
        $vanillaRows = @(
            $vanillaUses |
                Where-Object {
                    $_.ContextKey -eq $contextKey -and
                    (Test-VanillaUseTextMatch -VanillaUse $_ -Analysis $modRows[0])
                } |
                Sort-Object File, Line
        )
        if ($vanillaRows.Count -eq 0 -or $vanillaRows.Count -ne $modRows.Count) {
            continue
        }

        for ($index = 0; $index -lt $modRows.Count; $index++) {
            $analysis = $modRows[$index]
            $vanilla = $vanillaRows[$index]
            if (-not $gameById.ContainsKey($vanilla.ID)) {
                continue
            }
            if ($analysis.Ambiguous) {
                $resolved++
            }
            $analysis.GameRow = $gameById[$vanilla.ID]
            $analysis.MatchKind = "vanilla-source-sequence"
            $analysis.CandidateIDs = @(
                $vanillaRows.ID |
                    Sort-Object { [decimal]$_ } -Unique
            ) -join " | "
            $analysis.Ambiguous = $false
        }
    }
    return $resolved
}

$gameRows = @(Import-Csv -LiteralPath $GameCsv -Encoding UTF8)
$gameById = @{}
$gameByText = @{}
$gameByTranslation = @{}
foreach ($row in $gameRows) {
    if ($row.ID -notmatch '^\d+$') {
        continue
    }
    $gameById[$row.ID] = $row
    Add-ToLookup -Lookup $gameByText -Text $row.Text -Row $row
    Add-ToLookup -Lookup $gameByTranslation -Text $row.Translation -Row $row
}

$luaUses = @(Read-LuaUses)

if ($Mode -eq "Plan") {
    $pairGroups = @(
        $luaUses |
            Group-Object {
                Get-GroupKey `
                    -ID $_.ID `
                    -Text $_.Text `
                    -ContextKey (Get-UseContextKey -Use $_)
            } |
            Sort-Object {
                $first = $_.Group[0]
                ([decimal]$first.ID).ToString("00000000000000000000") +
                    [char]31 +
                    (Get-TextKey -Text $first.Text) +
                    [char]31 +
                    (Get-UseContextKey -Use $first)
            }
    )

    $analysisRows = New-Object "System.Collections.Generic.List[object]"
    foreach ($group in $pairGroups) {
        $first = $group.Group[0]
        $groupUses = @($group.Group | ForEach-Object { $_ })
        $activeUses = @($groupUses | Where-Object State -ne "dormant")
        $contextKey = Get-UseContextKey -Use $first
        $candidates = @(Get-GameCandidates -Text $first.Text)
        $selection = Select-GameCandidate `
            -OldID $first.ID `
            -OldText $first.Text `
            -Uses $groupUses `
            -Candidates $candidates

        $analysisRows.Add([pscustomobject]@{
            GroupKey          = Get-GroupKey `
                -ID $first.ID `
                -Text $first.Text `
                -ContextKey $contextKey
            ContextKey        = $contextKey
            OldID             = $first.ID
            OldText           = $first.Text
            Uses              = $groupUses
            ActiveOccurrences = $activeUses.Count
            GameRow           = $selection.Row
            MatchKind         = $selection.MatchKind
            CandidateIDs      = $selection.CandidateIDs
            Ambiguous         = $selection.Ambiguous
            Action            = ""
            NewID             = ""
            NewText           = ""
        })
    }

    $sourceResolved = Resolve-AmbiguitiesFromVanillaSource -Analyses $analysisRows
    $ambiguityRows = New-Object "System.Collections.Generic.List[object]"
    foreach ($analysis in @($analysisRows | Where-Object Ambiguous)) {
        $groupUses = @($analysis.Uses | ForEach-Object { $_ })
        $ambiguityRows.Add([pscustomobject]@{
            OldID        = $analysis.OldID
            SourceText   = $analysis.OldText
            ContextKey   = $analysis.ContextKey
            CandidateIDs = $analysis.CandidateIDs
            Comments     = @(
                $groupUses.Comment |
                    Where-Object { $_ } |
                    Sort-Object -Unique
            ) -join " | "
            Locations    = @(
                $groupUses |
                    Sort-Object Package, File, Line |
                    ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
            ) -join " | "
        })
    }
    $remainingByOldId = @{}
    foreach ($analysis in $analysisRows) {
        if ($null -ne $analysis.GameRow) {
            $analysis.Action = "restore-vanilla"
            $analysis.NewID = $analysis.GameRow.ID
            $analysis.NewText = $analysis.GameRow.Text
            continue
        }
        if (-not $remainingByOldId.ContainsKey($analysis.OldID)) {
            $remainingByOldId[$analysis.OldID] = New-Object "System.Collections.Generic.List[object]"
        }
        $remainingByOldId[$analysis.OldID].Add($analysis)
    }

    $usedIds = @{}
    foreach ($row in $gameRows) {
        if ($row.ID -match '^\d+$') {
            $usedIds[$row.ID] = $true
        }
    }
    foreach ($use in $luaUses) {
        $usedIds[$use.ID] = $true
    }
    foreach ($row in @(Import-Csv -LiteralPath $CatalogPath -Encoding UTF8)) {
        if ($row.ID -match '^\d+$') {
            $usedIds[$row.ID] = $true
        }
    }

    $nextId = $RangeStart
    foreach ($oldId in @($remainingByOldId.Keys | Sort-Object { [decimal]$_ })) {
        $remaining = @(
            $remainingByOldId[$oldId] |
                ForEach-Object { $_ }
        )
        $remainingTextKeys = @(
            $remaining |
                ForEach-Object { Get-TextKey -Text $_.OldText } |
                Sort-Object -Unique
        )
        $requiresNewId = (
            $gameById.ContainsKey($oldId) -or
            [decimal]$oldId -ge 9007199254740992 -or
            $remainingTextKeys.Count -gt 1
        )
        if (-not $requiresNewId) {
            continue
        }

        $textGroups = @(
            $remaining |
                Group-Object { Get-TextKey -Text $_.OldText } |
                Sort-Object Name
        )
        foreach ($textGroup in $textGroups) {
            while ($nextId -le $RangeEnd -and $usedIds.ContainsKey([string]$nextId)) {
                $nextId++
            }
            if ($nextId -gt $RangeEnd) {
                throw "Localization ID range is exhausted."
            }
            $newId = [string]$nextId
            foreach ($analysis in @(
                $textGroup.Group |
                    Sort-Object ContextKey
            )) {
                $analysis.Action = if ($analysis.Ambiguous) {
                    "assign-mod-id-ambiguous"
                }
                else {
                    "assign-mod-id"
                }
                $analysis.NewID = $newId
                $analysis.NewText = $analysis.OldText
            }
            $usedIds[$newId] = $true
            $nextId++
        }
    }

    $manifestRows = New-Object "System.Collections.Generic.List[object]"
    foreach ($analysis in $analysisRows) {
        if (-not $analysis.Action) {
            continue
        }
        if (
            $analysis.Action -eq "restore-vanilla" -and
            $analysis.OldID -eq $analysis.NewID -and
            (Normalize-LocalizationText $analysis.OldText) -eq
                (Normalize-LocalizationText $analysis.NewText)
        ) {
            continue
        }

        $uses = @($analysis.Uses | ForEach-Object { $_ })
        $locations = @(
            $uses |
                Sort-Object Package, File, Line |
                ForEach-Object { "$($_.Package):$($_.File):$($_.Line)" }
        )
        $manifestRows.Add([pscustomobject]@{
            Action            = $analysis.Action
            MatchKind         = $analysis.MatchKind
            ContextKey        = $analysis.ContextKey
            OldID             = $analysis.OldID
            NewID             = $analysis.NewID
            OldText           = $analysis.OldText
            NewText           = $analysis.NewText
            Occurrences       = $uses.Count
            ActiveOccurrences = $analysis.ActiveOccurrences
            Packages          = @($uses.Package | Sort-Object -Unique) -join " | "
            States            = @($uses.State | Sort-Object -Unique) -join " | "
            Locations         = $locations -join " | "
            GameLocation      = if ($null -ne $analysis.GameRow) {
                $analysis.GameRow.Context
            }
            else {
                ""
            }
            CandidateIDs      = $analysis.CandidateIDs
            Applied           = "no"
        })
    }

    Write-CsvUtf8 `
        -Path $ManifestPath `
        -Columns @(
            "Action",
            "MatchKind",
            "ContextKey",
            "OldID",
            "NewID",
            "OldText",
            "NewText",
            "Occurrences",
            "ActiveOccurrences",
            "Packages",
            "States",
            "Locations",
            "GameLocation",
            "CandidateIDs",
            "Applied"
        ) `
        -Rows $manifestRows

    Write-CsvUtf8 `
        -Path $AmbiguityPath `
        -Columns @(
            "OldID",
            "SourceText",
            "ContextKey",
            "CandidateIDs",
            "Comments",
            "Locations"
        ) `
        -Rows $ambiguityRows

    $restoreRows = @($manifestRows | Where-Object Action -eq "restore-vanilla")
    $newRows = @($manifestRows | Where-Object Action -like "assign-mod-id*")
    Write-Output "JAZZ localization clone/ID migration plan"
    Write-Output "Lua ID+text pairs: $($analysisRows.Count)"
    Write-Output "Restore vanilla pairs: $($restoreRows.Count); occurrences=$(($restoreRows | Measure-Object Occurrences -Sum).Sum)"
    Write-Output "Assign mod IDs: $($newRows.Count); occurrences=$(($newRows | Measure-Object Occurrences -Sum).Sum)"
    Write-Output "Keep unchanged pairs: $($analysisRows.Count - $manifestRows.Count)"
    Write-Output "Resolved by vanilla source sequence: $sourceResolved"
    Write-Output "Ambiguous vanilla matches: $($ambiguityRows.Count)"
    if ($newRows.Count -gt 0) {
        Write-Output "Allocated mod range: $($newRows[0].NewID)..$($newRows[-1].NewID)"
    }
    Write-Output "Manifest: $([IO.Path]::GetFullPath($ManifestPath))"
    Write-Output "Ambiguities: $([IO.Path]::GetFullPath($AmbiguityPath))"
    if ($ambiguityRows.Count -gt 0) {
        exit 3
    }
    exit 0
}

if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) {
    throw "Migration manifest does not exist: $ManifestPath"
}

$manifestRows = @(Import-Csv -LiteralPath $ManifestPath -Encoding UTF8)
if ($manifestRows.Count -eq 0) {
    throw "Migration manifest is empty."
}
if (Test-Path -LiteralPath $AmbiguityPath -PathType Leaf) {
    $ambiguities = @(Import-Csv -LiteralPath $AmbiguityPath -Encoding UTF8)
    if ($ambiguities.Count -gt 0) {
        throw "Cannot apply while ambiguous vanilla matches remain: $($ambiguities.Count)."
    }
}

$mappingByOldGroup = @{}
$expectedTextByNewId = @{}
$finalPairKeys = @{}
foreach ($row in $manifestRows) {
    if ($row.OldID -notmatch '^\d+$' -or $row.NewID -notmatch '^\d+$') {
        throw "Manifest contains a non-numeric ID."
    }
    if ([decimal]$row.NewID -ge 9007199254740992) {
        throw "Manifest NewID is not IEEE-754-safe: $($row.NewID)"
    }
    $oldGroupKey = Get-GroupKey `
        -ID $row.OldID `
        -Text $row.OldText `
        -ContextKey ([string]$row.ContextKey)
    if ($mappingByOldGroup.ContainsKey($oldGroupKey)) {
        throw (
            "Duplicate old ID+text+context group in manifest: " +
            "$($row.OldID) [$($row.ContextKey)]"
        )
    }
    $mappingByOldGroup[$oldGroupKey] = $row

    $newTextKey = Get-TextKey -Text $row.NewText
    if (
        $expectedTextByNewId.ContainsKey($row.NewID) -and
        $expectedTextByNewId[$row.NewID] -ne $newTextKey
    ) {
        throw "NewID $($row.NewID) maps to different final texts."
    }
    $expectedTextByNewId[$row.NewID] = $newTextKey
    $finalPairKeys[(Get-PairKey -ID $row.NewID -Text $row.NewText)] = $true
}

foreach ($use in $luaUses) {
    if ($expectedTextByNewId.ContainsKey($use.ID)) {
        $oldGroupKey = Get-GroupKey `
            -ID $use.ID `
            -Text $use.Text `
            -ContextKey (Get-UseContextKey -Use $use)
        if (
            -not $mappingByOldGroup.ContainsKey($oldGroupKey) -and
            $expectedTextByNewId[$use.ID] -ne (Get-TextKey -Text $use.Text)
        ) {
            throw "Final ID $($use.ID) is used by an unrelated text at $($use.Package):$($use.File):$($use.Line)."
        }
    }
}

$replacementsByFile = @{}
$seenOldGroups = @{}
$seenFinalPairs = @{}
foreach ($use in $luaUses) {
    $groupKey = Get-GroupKey `
        -ID $use.ID `
        -Text $use.Text `
        -ContextKey (Get-UseContextKey -Use $use)
    $pairKey = Get-PairKey -ID $use.ID -Text $use.Text
    if ($mappingByOldGroup.ContainsKey($groupKey)) {
        if (-not $replacementsByFile.ContainsKey($use.FullPath)) {
            $replacementsByFile[$use.FullPath] = New-Object "System.Collections.Generic.List[object]"
        }
        $mapping = $mappingByOldGroup[$groupKey]
        if (
            (Normalize-LocalizationText $mapping.OldText) -ne
            (Normalize-LocalizationText $mapping.NewText)
        ) {
            $replacementsByFile[$use.FullPath].Add([pscustomobject]@{
                Index  = $use.TextIndex
                Length = $use.TextLength
                Value  = ConvertTo-LuaQuotedText -Text $mapping.NewText -Quote $use.Quote
            })
        }
        if ($mapping.OldID -ne $mapping.NewID) {
            $replacementsByFile[$use.FullPath].Add([pscustomobject]@{
                Index  = $use.IDIndex
                Length = $use.IDLength
                Value  = $mapping.NewID
            })
        }
        $seenOldGroups[$groupKey] = $true
    }
    if ($finalPairKeys.ContainsKey($pairKey)) {
        $seenFinalPairs[$pairKey] = $true
    }
}

foreach ($row in $manifestRows) {
    $oldKey = Get-GroupKey `
        -ID $row.OldID `
        -Text $row.OldText `
        -ContextKey ([string]$row.ContextKey)
    $finalKey = Get-PairKey -ID $row.NewID -Text $row.NewText
    if (-not $seenOldGroups.ContainsKey($oldKey) -and -not $seenFinalPairs.ContainsKey($finalKey)) {
        throw "Manifest group is absent with both old and final representation: $($row.OldID) -> $($row.NewID)."
    }
}
$changedFiles = New-Object "System.Collections.Generic.List[string]"
$replacementCount = 0
foreach ($filePath in ($replacementsByFile.Keys | Sort-Object)) {
    $fileData = Read-Utf8File -Path $filePath
    $updated = $fileData.Text
    foreach ($replacement in @(
        $replacementsByFile[$filePath] |
            Sort-Object Index -Descending
    )) {
        $updated = $updated.Remove($replacement.Index, $replacement.Length).Insert(
            $replacement.Index,
            $replacement.Value
        )
        $replacementCount++
    }
    if ($updated -ne $fileData.Text) {
        Write-Utf8File -Path $filePath -Text $updated -HasBom $fileData.HasBom
        $changedFiles.Add($filePath)
    }
}

foreach ($row in $manifestRows) {
    $row.Applied = "yes"
}
Write-CsvUtf8 `
    -Path $ManifestPath `
    -Columns @(
        "Action",
        "MatchKind",
        "ContextKey",
        "OldID",
        "NewID",
        "OldText",
        "NewText",
        "Occurrences",
        "ActiveOccurrences",
        "Packages",
        "States",
        "Locations",
        "GameLocation",
        "CandidateIDs",
        "Applied"
    ) `
    -Rows $manifestRows

Write-Output "JAZZ localization clone/ID migration applied"
Write-Output "Manifest pairs: $($manifestRows.Count)"
Write-Output "Token replacements: $replacementCount"
Write-Output "Changed files: $($changedFiles.Count)"
foreach ($file in $changedFiles) {
    Write-Output "Changed: $file"
}
