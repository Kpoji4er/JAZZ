# Generate JA12 Medium/Low merc loot tiers from articles + wire Loot_JAZZ_* wrappers.
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding $false
$jazz = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz'
$units = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units'
$itemsPath = Join-Path $units 'items.lua'
$metaPath = Join-Path $units 'metadata.lua'
$docPath = Join-Path $jazz 'docs\technical\systems\ja12-merc-inventory-presets.md'

$alias = @{
  'HK G3' = 'G3A3'
  'HKG3' = 'G3A3'
  'G3' = 'G3A3'
  'M14' = 'M14SAW'
  'JAZZ_AMMO_308_Match' = 'JAZZ_AMMO_762x51_Match'
  'JAZZ_AMMO_308_FMJ' = 'JAZZ_AMMO_762x51_FMJ'
  'JazzArmor_NightCamoJacket' = 'JazzArmor_LeatherJacketBlk'
  'Detonator' = 'Combination_Detonator_Time'
  'NVGoggles' = $null  # omit — no reliable mod id
  'Radio' = $null
  'Scarf' = $null
  'US_Passport' = $null
  'Unarmed' = $null
}

# Parse article loot into structured entries
function ParseTierLine([string]$line) {
  $items = New-Object System.Collections.Generic.List[object]
  # qty marker may be × / x / * depending on source encoding
  $rx = [regex]('`([^`]+)`(?:(?:[xX*]|\u00D7)(\d+))?(?:\s*\(Double\))?')
  foreach ($m in $rx.Matches($line)) {
    $id = $m.Groups[1].Value.Trim()
    $qty = 1
    if ($m.Groups[2].Success -and $m.Groups[2].Value) { $qty = [int]$m.Groups[2].Value }
    $dbl = $m.Value -match '\(Double\)'
    # normalize aliases before stripping notes
    if ($id -match 'HK\s*G3') { $id = 'G3A3' }
    elseif ($alias.ContainsKey($id)) {
      $id = $alias[$id]
      if ($null -eq $id) { continue }
    }
    elseif ($id -match '^([A-Za-z0-9_]+)') { $id = $Matches[1] }
    if ($alias.ContainsKey($id)) {
      $mapped = $alias[$id]
      if ($null -eq $mapped) { continue }
      $id = $mapped
    }
    $items.Add([pscustomobject]@{ Id = $id; Qty = $qty; Double = $dbl }) | Out-Null
  }
  return $items
}

function IsAmmo([string]$id) { return $id -like 'JAZZ_AMMO_*' -or $id -like '*Grenade*' -or $id -eq 'JAZZ_AMMO_40mmFragGrenade' }
function IsFirearm([string]$id) {
  $melee = @('Knife','Knife_Sharpened','Knife_Balanced','Machete','Machete_Sharpened','Crowbar','Unarmed')
  if ($melee -contains $id) { return $false }
  if ($id -like 'JazzArmor_*') { return $false }
  if ($id -like 'Combination_*') { return $false }
  if ($id -in @('Lockpick','Wirecutter','Parts','Meds','FirstAidKit','Medkit','CombatStim','TNT','C4','PipeBomb','ShapedCharge','SmokeGrenade','FragGrenade','Detonator')) { return $false }
  if ($id -like 'JAZZ_CombatScope*') { return $false }
  if (IsAmmo $id) { return $false }
  # tools/explosives already filtered; remaining combat items are firearms/launchers
  return $true
}

$need = @(
  'Quinten','Vicious','Biff','Nervous','Flo','Cougar','Miguel','Gamos','Dynamo','Gaston','Horg','Manuel','Monk','Allik','Henning',
  'Static','Highball','Bull','Cord','Hobbit','Ricochet','Meat','Carlos','Devin','Shank','Vince','Hitman','Biggens','Kulba','Vilde','Grace','Steiger','Lucky','Laura','Eskimo'
)

$kits = @{} # name -> @{50=...;35=...;25=...;20=...}
$warnings = New-Object System.Collections.Generic.List[string]
$base = Join-Path $jazz 'docs\design\mercs-ja12'

foreach ($n in $need) {
  $slug = $n.ToLowerInvariant()
  $t = [IO.File]::ReadAllText((Join-Path $base "$slug.md"), [Text.Encoding]::UTF8)
  $tierMap = @{}
  foreach ($tier in @('50','35','25','20')) {
    $tierPat = '(?m)^\s*-\s*\*' + $tier + ':\s*(.+)$'
    if ($t -match $tierPat) {
      $entries = ParseTierLine $Matches[1]
      $guns = @($entries | Where-Object { IsFirearm $_.Id })
      $ammos = @($entries | Where-Object { $_.Id -like 'JAZZ_AMMO_*' })
      foreach ($g in $guns) {
        if ($g.Id -eq 'M79') {
          if (-not ($entries | Where-Object { $_.Id -eq 'JAZZ_AMMO_40mmFragGrenade' })) {
            [void]$warnings.Add("$n *${tier}: M79 without 40mm - adding x4")
            $entries.Add([pscustomobject]@{ Id = 'JAZZ_AMMO_40mmFragGrenade'; Qty = 4; Double = $false }) | Out-Null
          }
          continue
        }
        if ($ammos.Count -eq 0) {
          [void]$warnings.Add("$n *${tier}: firearm $($g.Id) without JAZZ_AMMO")
        }
      }
      $tierMap[$tier] = $entries
    } else {
      throw "Missing *$tier for $n"
    }
  }
  $kits[$n] = $tierMap
}

function EmitEntry($e) {
  if ($e.Double) {
    return "					PlaceObj('LootEntryInventoryItem', { Double = true, item = `"$($e.Id)`", stack_max = $($e.Qty), stack_min = $($e.Qty) }),"
  }
  if ($e.Qty -gt 1 -or ($e.Id -like 'JAZZ_AMMO_*') -or ($e.Id -in @('Meds','Parts','TNT','C4','PipeBomb','ShapedCharge','SmokeGrenade','FragGrenade','CombatStim','Knife','Knife_Sharpened','Knife_Balanced','HiPower','Colt1911'))) {
    return "					PlaceObj('LootEntryInventoryItem', { item = `"$($e.Id)`", stack_max = $($e.Qty), stack_min = $($e.Qty) }),"
  }
  # armor / single tools
  if ($e.Id -like 'JazzArmor_*' -or $e.Id -like 'Combination_*' -or $e.Id -like 'JAZZ_CombatScope*') {
    return "					PlaceObj('LootEntryInventoryItem', { item = `"$($e.Id)`" }),"
  }
  return "					PlaceObj('LootEntryInventoryItem', { item = `"$($e.Id)`", stack_max = 1, stack_min = 1 }),"
}

$sb = New-Object System.Text.StringBuilder
$metaSb = New-Object System.Text.StringBuilder
$docRows = New-Object System.Collections.Generic.List[string]

foreach ($n in $need) {
  foreach ($tier in @('50','35','25','20')) {
    $id = "JAZZ_${n}${tier}"
    [void]$sb.AppendLine("				PlaceObj('ModItemLootDef', {")
    [void]$sb.AppendLine("					Comment = `"merc`",")
    [void]$sb.AppendLine("					group = `"Mercs`",")
    [void]$sb.AppendLine("					id = `"$id`",")
    [void]$sb.AppendLine("					loot = `"all`",")
    $summary = @()
    foreach ($e in $kits[$n][$tier]) {
      [void]$sb.AppendLine((EmitEntry $e))
      $bit = $e.Id
      if ($e.Qty -gt 1) { $bit += "×$($e.Qty)" }
      if ($e.Double) { $bit += ' (Double)' }
      $summary += $bit
    }
    [void]$sb.AppendLine("				}),")
    [void]$metaSb.AppendLine("		PlaceObj('ModResourcePreset', {")
    [void]$metaSb.AppendLine("			'Class', `"LootDef`",")
    [void]$metaSb.AppendLine("			'Id', `"$id`",")
    [void]$metaSb.AppendLine("			'ClassDisplayName', `"Loot definition`",")
    [void]$metaSb.AppendLine("		}),")
    if ($tier -eq '50') {
      $docRows.Add("| $n | ``Loot_JAZZ_$n`` | $($summary -join ', ') |")
    }
  }
}

# Build wrappers
$wrapSb = New-Object System.Text.StringBuilder
foreach ($n in $need) {
  [void]$wrapSb.AppendLine("				PlaceObj('ModItemLootDef', {")
  [void]$wrapSb.AppendLine("					Comment = `"merc`",")
  [void]$wrapSb.AppendLine("					group = `"Mercs`",")
  [void]$wrapSb.AppendLine("					id = `"Loot_JAZZ_$n`",")
  [void]$wrapSb.AppendLine("					PlaceObj('LootEntryLootDef', { loot_def = `"JAZZ_${n}50`", weight = 50000 }),")
  [void]$wrapSb.AppendLine("					PlaceObj('LootEntryLootDef', { loot_def = `"JAZZ_${n}35`", weight = 35000 }),")
  [void]$wrapSb.AppendLine("					PlaceObj('LootEntryLootDef', { loot_def = `"JAZZ_${n}25`", weight = 25000 }),")
  [void]$wrapSb.AppendLine("					PlaceObj('LootEntryLootDef', { loot_def = `"JAZZ_${n}20`", weight = 20000 }),")
  [void]$wrapSb.AppendLine("				}),")
}

$u = [IO.File]::ReadAllText($itemsPath, [Text.Encoding]::UTF8)

# Replace knife stubs only if still knives
foreach ($n in $need) {
  $pat = "(?s)PlaceObj\('ModItemLootDef', \{\s*Comment = `"merc`",\s*group = `"Mercs`",\s*id = `"Loot_JAZZ_$n`",\s*PlaceObj\('LootEntryInventoryItem', \{\s*item = `"Knife`",\s*stack_max = 1,\s*stack_min = 1,\s*\}\),\s*\}\),"
  $repl = @"
PlaceObj('ModItemLootDef', {
					Comment = "merc",
					group = "Mercs",
					id = "Loot_JAZZ_$n",
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${n}50", weight = 50000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${n}35", weight = 35000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${n}25", weight = 25000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${n}20", weight = 20000 }),
				}),
"@
  $nu = [regex]::Replace($u, $pat, $repl.TrimEnd(), 1)
  if ($nu -ne $u) { $u = $nu; Write-Host "wrapped Loot_JAZZ_$n" }
}

# Always refresh tier preset bodies for these mercs (replace existing block range)
$first = 'JAZZ_Quinten50'
$last = 'JAZZ_Eskimo20'
if ($u -match [regex]::Escape("id = `"$first`"")) {
  $start = [regex]::Match($u, "(?s)PlaceObj\('ModItemLootDef', \{\s*Comment = `"merc`",\s*group = `"Mercs`",\s*id = `"$first`",")
  $end = [regex]::Match($u, "(?s)PlaceObj\('ModItemLootDef', \{\s*Comment = `"merc`",\s*group = `"Mercs`",\s*id = `"$last`",.*?\}\),")
  if (-not $start.Success -or -not $end.Success) { throw 'cannot locate Quinten50..Eskimo20 block' }
  $from = $start.Index
  $to = $end.Index + $end.Length
  $u = $u.Remove($from, $to - $from).Insert($from, $sb.ToString().TrimEnd() + "`r`n")
  Write-Host 'Replaced tier preset block Quinten50..Eskimo20'
} else {
  $m = [regex]::Match($u, "(?s)PlaceObj\('ModItemLootDef', \{\s*Comment = `"merc`",\s*group = `"Mercs`",\s*id = `"JAZZ_Rothman20`",.*?\}\),")
  if (-not $m.Success) { throw 'JAZZ_Rothman20 anchor missing' }
  $u = $u.Insert($m.Index + $m.Length, "`r`n" + $sb.ToString())
  Write-Host 'Inserted tier presets'
}

[IO.File]::WriteAllText($itemsPath, $u, $utf8)

# metadata
$meta = [IO.File]::ReadAllText($metaPath, [Text.Encoding]::UTF8)
if ($meta -notmatch 'JAZZ_Quinten50') {
  $gm = [regex]::Match($meta, "PlaceObj\('ModResourcePreset', \{\s*'Class', `"LootDef`",\s*'Id', `"Loot_JAZZ_Eskimo`",\s*'ClassDisplayName', `"Loot definition`",\s*\}\),")
  if (-not $gm.Success) {
    $gm = [regex]::Match($meta, "PlaceObj\('ModResourcePreset', \{\s*'Class', `"LootDef`",\s*'Id', `"Loot_JAZZ_Grom`",\s*'ClassDisplayName', `"Loot definition`",\s*\}\),")
  }
  if ($gm.Success) {
    $meta = $meta.Insert($gm.Index + $gm.Length, "`r`n" + $metaSb.ToString())
  } else {
    # append after last Loot_JAZZ_Rothman resource if any
    $gm = [regex]::Match($meta, "PlaceObj\('ModResourcePreset', \{\s*'Class', `"LootDef`",\s*'Id', `"JAZZ_Rothman20`",\s*'ClassDisplayName', `"Loot definition`",\s*\}\),")
    if (-not $gm.Success) { throw 'meta loot anchor missing' }
    $meta = $meta.Insert($gm.Index + $gm.Length, "`r`n" + $metaSb.ToString())
  }
  [IO.File]::WriteAllText($metaPath, $meta, $utf8)
  Write-Host 'metadata updated'
} else {
  Write-Host 'metadata already has Quinten50'
}

# Also register Loot_JAZZ_* wrappers if missing as resources (they may already exist from knife era)
foreach ($n in $need) {
  $lid = "Loot_JAZZ_$n"
  if ($meta -notmatch [regex]::Escape("'Id', `"$lid`"")) {
    $extra = "		PlaceObj('ModResourcePreset', {`r`n			'Class', `"LootDef`",`r`n			'Id', `"$lid`",`r`n			'ClassDisplayName', `"Loot definition`",`r`n		}),`r`n"
    $meta = [IO.File]::ReadAllText($metaPath, [Text.Encoding]::UTF8)
    $gm = [regex]::Match($meta, "PlaceObj\('ModResourcePreset', \{\s*'Class', `"LootDef`",\s*'Id', `"JAZZ_${n}20`",\s*'ClassDisplayName', `"Loot definition`",\s*\}\),")
    if ($gm.Success) {
      $meta = $meta.Insert($gm.Index + $gm.Length, "`r`n" + $extra)
      [IO.File]::WriteAllText($metaPath, $meta, $utf8)
    }
  }
}

Write-Host 'Warnings:'
$warnings | Select-Object -Unique | ForEach-Object { Write-Host " - $_" }

# Doc
$highDoc = @'
| Merc | Root | *50 summary (see items.lua for 35/25/20) |
| --- | --- | --- |
| Colby | `Loot_JAZZ_Colby` | MP5A4 + 9x19×60, shaped/C4, leather vest, smoke, remote detonator |
| Blade | `Loot_JAZZ_Blade` | (article tiers in items.lua) |
| Ira | `Loot_JAZZ_Ira` | (article tiers in items.lua) |
| Dimitri | `Loot_JAZZ_Dimitri` | (article tiers in items.lua) |
| Madman | `Loot_JAZZ_Madman` | (article tiers in items.lua) |
| Conrad | `Loot_JAZZ_Conrad` | (article tiers in items.lua) |
| Mike | `Loot_JAZZ_Mike` | (article tiers in items.lua) |
| Grom | `Loot_JAZZ_Grom` | (article tiers in items.lua) |
| Rothman | `Loot_JAZZ_Rothman` | FNFAL + 7.62×51 Match×40 (Double), uniform, shaped charge, FAK |
'@

# Enrich high from items quickly for doc accuracy - optional leave as is and focus on new

$doc = @"
# JA12 merc inventory presets

Current-state loot for AIM/MERC hire kits from the JA12 wave. Root def ``Loot_JAZZ_<Nick>`` rolls weighted child defs ``JAZZ_<Nick>50/35/25/20`` (weights 50k/35k/25k/20k).

## Rules

- Every firearm / grenade launcher tier includes matching ``JAZZ_AMMO_*`` (or ``JAZZ_AMMO_40mmFragGrenade`` for M79).
- Ammo marked Double in design articles uses ``Double = true`` on the loot entry.
- Melee-only kits (Vicious, Ricochet, Shank, Dynamo crowbar, Meat explosives) may omit ammo.
- ID aliases applied at generate time: ``HK G3``→``G3A3``, ``M14``→``M14SAW``, ``JAZZ_AMMO_308_*``→``JAZZ_AMMO_762x51_*``, ``JazzArmor_NightCamoJacket``→``JazzArmor_LeatherJacketBlk``, bare ``Detonator``→``Combination_Detonator_Time``.
- Omitted (no stable mod id): ``NVGoggles``, ``Radio``, ``Scarf``, ``US_Passport``, ``Unarmed``.

Source of truth for intended kits: ``docs/design/mercs-ja12/<slug>.md`` loot section. Runtime: ``jazz-units/items.lua``.

## High + Rothman (already shipped)

$highDoc

## Medium / Low (filled from articles)

| Merc | Root | *50 contents |
| --- | --- | --- |
$($docRows -join "`r`n")

## Child preset IDs

For each merc above: ``JAZZ_<Nick>50``, ``JAZZ_<Nick>35``, ``JAZZ_<Nick>25``, ``JAZZ_<Nick>20``.

## Generate notes

Regenerate Medium/Low knife stubs via ``.agents/scripts/`` only when articles change; keep ammo pairing invariant.
"@

[IO.File]::WriteAllText($docPath, $doc, $utf8)
Write-Host "Wrote $docPath"

# verify Bull wrapper + Bull50
$u2 = [IO.File]::ReadAllText($itemsPath, [Text.Encoding]::UTF8)
Write-Host ('Bull50: ' + ($u2 -match 'id = "JAZZ_Bull50"'))
Write-Host ('Bull wrapper tiers: ' + ($u2 -match 'loot_def = "JAZZ_Bull50"'))
$idx = $u2.IndexOf('id = "JAZZ_Bull50"')
Write-Host $u2.Substring($idx, [Math]::Min(450, $u2.Length-$idx))
