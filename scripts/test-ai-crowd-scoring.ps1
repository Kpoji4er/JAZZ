[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-CrowdPenalty {
    param(
        [double]$Distance,
        [int]$SameTile,
        [int]$Adjacent,
        [int]$Outer
    )

    if ($Distance -lt 1) { return $SameTile }
    if ($Distance -lt 2) { return $Adjacent }
    if ($Distance -lt 3) { return $Outer }
    return 0
}

function Get-CrowdModifier {
    param(
        [double[]]$Live = @(),
        [double[]]$Casualties = @(),
        [switch]$Melee,
        [switch]$Healer
    )

    if ($Healer) {
        return 100
    }

    $danger = 0
    foreach ($distance in $Live) {
        $danger += Get-CrowdPenalty -Distance $distance -SameTile 60 -Adjacent 25 -Outer 10
    }

    $casualtyCount = 0
    foreach ($distance in $Casualties) {
        $penalty = Get-CrowdPenalty -Distance $distance -SameTile 45 -Adjacent 30 -Outer 15
        if ($penalty -gt 0) {
            $danger += $penalty
            $casualtyCount++
        }
    }
    if ($casualtyCount -gt 1) {
        $danger += 10 * ($casualtyCount - 1)
    }

    $minimum = if ($Melee) { 55 } else { 25 }
    return [Math]::Min(100, [Math]::Max($minimum, 100 - $danger))
}

function Get-CoverSpacingModifier {
    param(
        [int]$NearCoveredAllies = 0,
        [switch]$Medic
    )
    if ($Medic) { return 100 }
    if ($NearCoveredAllies -le 0) { return 100 }
    if ($NearCoveredAllies -eq 1) { return 55 }
    return 30
}

function Assert-Equal {
    param([string]$Name, $Actual, $Expected)
    if ($Actual -ne $Expected) {
        throw "$Name failed: expected=$Expected actual=$Actual"
    }
}

Assert-Equal 'isolated' (Get-CrowdModifier) 100
Assert-Equal 'one adjacent live' (Get-CrowdModifier -Live 1) 75
Assert-Equal 'two adjacent live' (Get-CrowdModifier -Live 1, 1) 50
Assert-Equal 'one same-voxel casualty' (Get-CrowdModifier -Casualties 0) 55
Assert-Equal 'two same-voxel casualties' (Get-CrowdModifier -Casualties 0, 0) 25
Assert-Equal 'one adjacent casualty' (Get-CrowdModifier -Casualties 1) 70
Assert-Equal 'dense melee floor' (Get-CrowdModifier -Live 0, 0 -Casualties 0, 0 -Melee) 55
Assert-Equal 'dense healer exempt' (Get-CrowdModifier -Live 0, 0 -Casualties 0, 0 -Healer) 100
Assert-Equal 'outer casualty band' (Get-CrowdModifier -Casualties 2) 85
Assert-Equal 'outside radius' (Get-CrowdModifier -Live 3 -Casualties 3) 100
Assert-Equal 'cover free' (Get-CoverSpacingModifier -NearCoveredAllies 0) 100
Assert-Equal 'cover one neighbor' (Get-CoverSpacingModifier -NearCoveredAllies 1) 55
Assert-Equal 'cover two neighbors' (Get-CoverSpacingModifier -NearCoveredAllies 2) 30
Assert-Equal 'cover medic exempt' (Get-CoverSpacingModifier -NearCoveredAllies 2 -Medic) 100

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourcePath = Join-Path $repoRoot 'Code\CombatAI.lua'
$source = [IO.File]::ReadAllText($sourcePath, [Text.Encoding]::UTF8)

$required = @(
    'function JazzAI_CrowdDangerModifier(context, dest)',
    'local crowd_mod = JazzAI_CrowdDangerModifier(context, dest)',
    'CROWD/DANGER MOD (%)',
    'function JazzAI_CoverSpacingModifier(context, dest)',
    'local cover_mod = JazzAI_CoverSpacingModifier(context, dest)',
    'COVER SPACING MOD (%)',
    'JazzAI_IsMedicCrowdExempt',
    'remove = dx == cx and dy == cy and dz == cz'
)
foreach ($needle in $required) {
    if (-not $source.Contains($needle)) {
        throw "Missing source contract: $needle"
    }
}

if ($source.Contains('local spacing = JazzAI_AllySpacingScore(context, dest)')) {
    throw 'Legacy global additive ally-spacing call is still active in AIScoreDest.'
}

$callNeedle = 'local crowd_mod = JazzAI_CrowdDangerModifier(context, dest)'
$callCount = ([regex]::Matches($source, [regex]::Escape($callNeedle))).Count
Assert-Equal 'single AIScoreDest integration' $callCount 1

$helperStart = $source.IndexOf('function JazzAI_CrowdDangerModifier(context, dest)')
$scoreStart = $source.IndexOf('function AIScoreDest(', $helperStart)
if ($helperStart -lt 0 -or $scoreStart -le $helperStart) {
    throw 'Unable to isolate CrowdDanger helper source.'
}
$helperSource = $source.Substring($helperStart, $scoreStart - $helperStart)
foreach ($forbidden in @('InteractionRand', 'AsyncRand', 'MapVar(', 'GameVar(', 'MapGet(')) {
    if ($helperSource.Contains($forbidden)) {
        throw "Non-deterministic or persistent dependency in helper: $forbidden"
    }
}

$biasStart = $source.IndexOf('-- apply modifiers from bias markers at the end', $scoreStart)
$crowdCall = $source.IndexOf($callNeedle, $scoreStart)
$coverNeedle = 'local cover_mod = JazzAI_CoverSpacingModifier(context, dest)'
$coverCall = $source.IndexOf($coverNeedle, $crowdCall)
$scoreEnd = $source.IndexOf('ResumeInfiniteLoopDetection("AiCalc")', $coverCall)
if ($biasStart -lt 0 -or $crowdCall -le $biasStart -or $coverCall -le $crowdCall -or $scoreEnd -le $coverCall) {
    throw 'Crowd then cover-spacing modifiers must run once after BiasMarker scoring and before AIScoreDest returns.'
}

Write-Host 'AI crowd scoring checks passed: model=14, source=integrated, determinism=static'
