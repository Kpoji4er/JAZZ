$ErrorActionPreference = 'Stop'
$unitsRoot = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units'
$items = Join-Path $unitsRoot 'items.lua'
$content = Get-Content -LiteralPath $items -Raw

# Extract ModItemAIArchetype blocks roughly by matching PlaceObj and following id=
$pattern = "PlaceObj\('ModItemAIArchetype',\s*\{([\s\S]*?)\n\t\t\t\}\),"
# Fallback: find line numbers then scan forward for id/group
$lines = Get-Content -LiteralPath $items
$starts = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
  if ($lines[$i] -match "PlaceObj\('ModItemAIArchetype'") {
    $starts += $i
  }
}
Write-Host "ModItemAIArchetype count: $($starts.Count)"
$archetypes = @()
foreach ($s in $starts) {
  $id = $null; $group = $null; $comment = $null
  $behaviors = @(); $sigCount = 0; $optLoc = $false
  $end = [Math]::Min($s + 800, $lines.Count - 1)
  # Find matching end: next PlaceObj ModItemAIArchetype or closing of folder-ish - use first occurrence of id = after PrefStance-ish
  for ($j = $s; $j -le $end; $j++) {
    if ($lines[$j] -match "^\s+id = `"([^`"]+)`",?\s*$") { $id = $Matches[1] }
    if ($lines[$j] -match "^\s+group = `"([^`"]+)`",?\s*$") { $group = $Matches[1] }
    if ($lines[$j] -match "^\s+Comment = `"([^`"]*)`"") { $comment = $Matches[1] }
    if ($lines[$j] -match "PlaceObj\('(StandardAI|PositioningAI|HoldPositionAI|CustomAI)") { $behaviors += $Matches[1] }
    if ($lines[$j] -match "PlaceObj\('AIAction") { $sigCount++ }
    if ($j -gt $s -and $lines[$j] -match "PlaceObj\('ModItemAIArchetype'") { break }
    # Stop when we hit id= that looks like end of this object: after TargetScoreRandomization typically id comes last
  }
  # Prefer last id/group before next archetype start
  $id = $null; $group = $null
  $nextStart = if (($starts.IndexOf($s) + 1) -lt $starts.Count) { $starts[$starts.IndexOf($s)+1] } else { [Math]::Min($s+1200, $lines.Count) }
  for ($j = $s; $j -lt $nextStart; $j++) {
    if ($lines[$j] -match "^\s+id = `"([^`"]+)`",?\s*$") { $id = $Matches[1] }
    if ($lines[$j] -match "^\s+group = `"([^`"]+)`",?\s*$") { $group = $Matches[1] }
    if ($lines[$j] -match "^\s+Comment = `"([^`"]*)`"") { $comment = $Matches[1] }
  }
  $archetypes += [pscustomobject]@{ Line = $s+1; Id = $id; Group = $group; Comment = $comment }
}
$archetypes | Format-Table -AutoSize | Out-String -Width 200 | Write-Host

# UnitData pattern classification
$unitDir = Join-Path $unitsRoot 'UnitData'
$files = Get-ChildItem -LiteralPath $unitDir -Filter '*.lua'
$stats = [ordered]@{
  total_with_pick = 0
  empty_stub = 0
  deserter = 0
  anger_melee = 0
  anger_assaulter = 0
  medic_switch = 0
  mortar_scared = 0
  gl_ordnance = 0
  commander_soldier = 0
  stealth_hide = 0
  unique = 0
  has_reposition = 0
}
$byBase = @{}
$byRepo = @{}
$patternHits = @{
  empty_stub = @()
  deserter = @()
  anger_melee = @()
  anger_assaulter = @()
  medic_switch = @()
  mortar_scared = @()
  gl_ordnance = @()
  commander_soldier = @()
  unique = @()
}

foreach ($f in $files) {
  $t = Get-Content -LiteralPath $f.FullName -Raw
  if ($t -notmatch 'PickCustomArchetype') { continue }
  $stats.total_with_pick++
  $base = $null
  if ($t -match '(?m)^\s*archetype = "([^"]+)",') { $base = $Matches[1] }
  if (-not $byBase.ContainsKey($base)) { $byBase[$base] = @() }
  $byBase[$base] += $f.BaseName
  if ($t -match '(?m)^\s*RepositionArchetype = "([^"]+)",') {
    $stats.has_reposition++
    $r = $Matches[1]
    if (-not $byRepo.ContainsKey($r)) { $byRepo[$r] = @() }
    $byRepo[$r] += $f.BaseName
  }

  $classified = $false
  if ($t -match 'PickCustomArchetype = function \(self, proto_context\)\s+end') {
    $stats.empty_stub++; $patternHits.empty_stub += $f.BaseName; $classified = $true
  }
  $hasDeserter = $t -match 'archetype = "Deserter"'
  $hasMedic = $t -match 'archetype = "Medic"'
  $hasMelee = $t -match 'archetype = "Melee"'
  $hasAssaulter = $t -match 'archetype = "Legion_Assaulter"'
  $hasAngry = $t -match 'AIArchetypeAngry'
  $hasScared = $t -match 'AIArchetypeScared'
  $hasGL = $t -match 'GrenadeLauncher|PrimaryNonGL'
  $hasCommander = $t -match 'archetype = "Soldier"' -and $t -match 'ArmyCommander|Commander'
  $hasStealth = $t -match 'CanStealth|Hide\(\)'

  if ($hasDeserter) { $stats.deserter++; $patternHits.deserter += $f.BaseName; $classified = $true }
  if ($hasMedic) { $stats.medic_switch++; $patternHits.medic_switch += $f.BaseName; $classified = $true }
  if ($hasMelee -and $hasAngry) { $stats.anger_melee++; $patternHits.anger_melee += $f.BaseName; $classified = $true }
  elseif ($hasAssaulter -and ($hasAngry -or $t -match 'dist < 10\*const\.SlabSizeX')) {
    # many legion units switch to assaulter without Melee archetype
    if (-not $hasMelee) { $stats.anger_assaulter++; $patternHits.anger_assaulter += $f.BaseName; $classified = $true }
  }
  if ($hasScared -and ($t -match 'Mortar|Artillery|Underground')) { $stats.mortar_scared++; $patternHits.mortar_scared += $f.BaseName; $classified = $true }
  if ($hasGL) { $stats.gl_ordnance++; $patternHits.gl_ordnance += $f.BaseName; $classified = $true }
  if ($f.BaseName -match 'ArmyCommander' -and $t -match 'archetype = "Soldier"') {
    $stats.commander_soldier++; $patternHits.commander_soldier += $f.BaseName; $classified = $true
  }
  if ($hasStealth) { $stats.stealth_hide++ }
  if (-not $classified) { $stats.unique++; $patternHits.unique += $f.BaseName }
}

Write-Host "`n=== Pattern stats ==="
$stats.GetEnumerator() | ForEach-Object { Write-Host "$($_.Key): $($_.Value)" }

Write-Host "`n=== Base archetype usage (units with PickCustom OR all UnitData) ==="
# recount all units with archetype field
$allBase = @{}
$allRepo = @{}
foreach ($f in $files) {
  $t = Get-Content -LiteralPath $f.FullName -Raw
  if ($t -match '(?m)^\s*archetype = "([^"]+)",') {
    $b = $Matches[1]
    if (-not $allBase.ContainsKey($b)) { $allBase[$b] = 0 }
    $allBase[$b]++
  }
  if ($t -match '(?m)^\s*RepositionArchetype = "([^"]+)",') {
    $r = $Matches[1]
    if (-not $allRepo.ContainsKey($r)) { $allRepo[$r] = 0 }
    $allRepo[$r]++
  }
}
Write-Host "Base archetypes:"
$allBase.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object { Write-Host ("  {0,3} {1}" -f $_.Value, $_.Key) }
Write-Host "RepositionArchetype:"
$allRepo.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object { Write-Host ("  {0,3} {1}" -f $_.Value, $_.Key) }

Write-Host "`n=== Pattern member lists (abbrev) ==="
foreach ($k in $patternHits.Keys) {
  Write-Host "$k ($($patternHits[$k].Count)): $($patternHits[$k] -join ', ')"
}
