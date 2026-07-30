#Requires -Version 5.1
<#
.SYNOPSIS
  Fail if any Lua short string ("..." / '...') contains a raw newline.

.DESCRIPTION
  JA3 loads mod Lua and reports "unfinished string" if a short string spans a real line break.
  Multiline text must use \n escapes or long brackets [[...]] / [=[...]=].
#>
[CmdletBinding()]
param(
    [string]$Root = '',
    [string[]]$Include = @('InventoryItem', 'Code', 'CharacterEffect', 'Const', 'XTemplate', 'UnitData', 'items.lua', 'metadata.lua')
)

$ErrorActionPreference = 'Stop'

if (-not $Root) {
    $scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
    $Root = (Resolve-Path (Join-Path $scriptDir '..')).Path
}

function Get-ScanTargets {
    param([string]$RootPath, [string[]]$IncludePaths)
    $files = New-Object System.Collections.Generic.List[string]
    foreach ($rel in $IncludePaths) {
        $full = Join-Path $RootPath $rel
        if (Test-Path -LiteralPath $full -PathType Leaf) {
            if ($full -like '*.lua') { [void]$files.Add((Resolve-Path -LiteralPath $full).Path) }
            continue
        }
        if (-not (Test-Path -LiteralPath $full -PathType Container)) { continue }
        Get-ChildItem -LiteralPath $full -Recurse -File -Filter '*.lua' | ForEach-Object {
            [void]$files.Add($_.FullName)
        }
    }
    return @($files | Sort-Object -Unique)
}

function Find-UnfinishedShortStrings {
    param([string]$Path)
    $text = [IO.File]::ReadAllText($Path)
    $issues = New-Object System.Collections.Generic.List[object]
    $i = 0
    $n = $text.Length
    $line = 1
    $state = 'normal' # normal | line_comment | dquote | squote | long_string | long_comment
    $longEq = 0
    $stringStartLine = 0
    $BS = [char]92
    $DQ = [char]34
    $SQ = [char]39
    $LB = [char]91
    $RB = [char]93
    $EQ = [char]61
    $DASH = [char]45

    while ($i -lt $n) {
        $ch = $text[$i]
        $next = if ($i + 1 -lt $n) { $text[$i + 1] } else { [char]0 }

        if ($state -eq 'normal') {
            if ($ch -eq $DASH -and $next -eq $DASH) {
                if ($i + 2 -lt $n -and $text[$i + 2] -eq $LB) {
                    $eq = 0
                    $j = $i + 3
                    while ($j -lt $n -and $text[$j] -eq $EQ) { $eq++; $j++ }
                    if ($j -lt $n -and $text[$j] -eq $LB) {
                        $state = 'long_comment'
                        $longEq = $eq
                        $i = $j + 1
                        continue
                    }
                }
                $state = 'line_comment'
                $i += 2
                continue
            }
            if ($ch -eq $LB) {
                $eq = 0
                $j = $i + 1
                while ($j -lt $n -and $text[$j] -eq $EQ) { $eq++; $j++ }
                if ($j -lt $n -and $text[$j] -eq $LB) {
                    $state = 'long_string'
                    $longEq = $eq
                    $i = $j + 1
                    continue
                }
            }
            if ($ch -eq $DQ) {
                $state = 'dquote'
                $stringStartLine = $line
                $i++
                continue
            }
            if ($ch -eq $SQ) {
                $state = 'squote'
                $stringStartLine = $line
                $i++
                continue
            }
            if ($ch -eq "`n") { $line++ }
            $i++
            continue
        }

        if ($state -eq 'line_comment') {
            if ($ch -eq "`n") {
                $state = 'normal'
                $line++
            }
            $i++
            continue
        }

        if ($state -eq 'long_comment' -or $state -eq 'long_string') {
            if ($ch -eq $RB) {
                $eq = 0
                $j = $i + 1
                while ($j -lt $n -and $text[$j] -eq $EQ) { $eq++; $j++ }
                if ($eq -eq $longEq -and $j -lt $n -and $text[$j] -eq $RB) {
                    $state = 'normal'
                    $i = $j + 1
                    continue
                }
            }
            if ($ch -eq "`n") { $line++ }
            $i++
            continue
        }

        if ($state -eq 'dquote' -or $state -eq 'squote') {
            $close = if ($state -eq 'dquote') { $DQ } else { $SQ }
            if ($ch -eq $BS) {
                # Skip escaped char; a literal escaped newline is still invalid in Lua short strings,
                # but treat "\n" digraph (backslash + n) as content.
                if ($i + 1 -lt $n) {
                    if ($text[$i + 1] -eq "`n") { $line++ }
                    $i += 2
                } else {
                    $i++
                }
                continue
            }
            if ($ch -eq $close) {
                $state = 'normal'
                $i++
                continue
            }
            if ($ch -eq "`n" -or $ch -eq "`r") {
                $kind = if ($state -eq 'dquote') { '"..."' } else { "'...'" }
                [void]$issues.Add([pscustomobject]@{
                        Path = $Path
                        Line = $stringStartLine
                        Message = "Unfinished short string $kind (raw newline). Use \n or [[...]]."
                    })
                $state = 'normal'
                if ($ch -eq "`r" -and $next -eq "`n") { $i += 2 } else { $i++ }
                $line++
                continue
            }
            $i++
            continue
        }

        $i++
    }

    if ($state -eq 'dquote' -or $state -eq 'squote') {
        $kind = if ($state -eq 'dquote') { '"..."' } else { "'...'" }
        [void]$issues.Add([pscustomobject]@{
                Path = $Path
                Line = $stringStartLine
                Message = "Unfinished short string $kind at EOF."
            })
    }

    return $issues
}

$targets = Get-ScanTargets -RootPath $Root -IncludePaths $Include
Write-Output ("JAZZ Lua short-string check: {0} file(s)" -f $targets.Count)

$all = New-Object System.Collections.Generic.List[object]
foreach ($file in $targets) {
    foreach ($issue in (Find-UnfinishedShortStrings -Path $file)) {
        [void]$all.Add($issue)
    }
}

if ($all.Count -eq 0) {
    Write-Output 'OK: no unfinished short strings.'
    exit 0
}

$rootFull = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\', '/')
foreach ($issue in $all) {
    $rel = $issue.Path
    if ($rel.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase)) {
        $rel = $rel.Substring($rootFull.Length).TrimStart('\', '/')
    }
    Write-Output ("FAIL: {0}:{1}: {2}" -f $rel, $issue.Line, $issue.Message)
}

Write-Error ("Found {0} unfinished Lua short string(s)." -f $all.Count)
exit 1
