# Wire Medium/Low JA12 mercs into jazz-units/jazz items.lua + metadata.lua
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding $false
$jazz = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not (Test-Path (Join-Path $jazz 'AGENTS.md'))) {
  $jazz = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz'
}
$units = Join-Path (Split-Path $jazz -Parent) 'jazz-units'
$missing = @(
  'Rothman','Quinten','Vicious','Biff','Nervous','Flo','Cougar','Miguel','Gamos','Dynamo',
  'Gaston','Horg','Manuel','Monk','Allik','Henning','Static','Highball','Bull','Cord',
  'Hobbit','Ricochet','Meat','Carlos','Devin','Shank','Vince','Hitman','Biggens','Kulba',
  'Vilde','Grace','Steiger','Lucky','Laura','Eskimo'
)

function ConvertCompanionToModItemFields([string]$body) {
  # Convert DefineClass-style "Key = value" to ModItem "'Key', value" (skip already-quoted keys)
  $lines = $body -split "`r?`n"
  $out = New-Object System.Collections.Generic.List[string]
  foreach ($line in $lines) {
    if ($line -match '^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
      $indent = $Matches[1]
      $key = $Matches[2]
      $rest = $Matches[3]
      # skip __parents / __generated
      if ($key -like '__*') { continue }
      $out.Add("${indent}'${key}', $rest") | Out-Null
    } else {
      $out.Add($line) | Out-Null
    }
  }
  return ($out -join "`r`n")
}

function ExtractDefineBody([string]$path) {
  $t = [IO.File]::ReadAllText($path, [Text.Encoding]::UTF8)
  # from object_class = "UnitData", to last closing of DefineClass
  $m = [regex]::Match($t, '(?s)object_class\s*=\s*"UnitData"\s*,\s*(.*)\r?\n\}\s*$')
  if (-not $m.Success) { throw "Cannot parse $path" }
  return $m.Groups[1].Value.TrimEnd()
}

function GetField([string]$t, [string]$name) {
  if ($t -match "(?m)^\s*$name\s*=\s*`"([^`"]*)`"") { return $Matches[1] }
  if ($t -match "(?m)^\s*$name\s*=\s*T\([^`"]*`"([^`"]*)`"") { return $Matches[1] }
  return $null
}

$maleApp = @'
		PlaceObj('ModItemAppearancePreset', {
			Armor = "",
			ArmorColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(0, 0, 0, 255),
				'EditableColor2', RGBA(0, 0, 0, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			Body = "Faction_Militia_Top_03",
			BodyColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(12, 5, 5, 255),
				'EditableRoughness1', 3,
				'EditableMetallic1', 10,
				'EditableColor2', RGBA(47, 47, 47, 255),
				'EditableColor3', RGBA(25, 36, 25, 255),
			}),
			Chest = "Faction_Acc_Heavy_02",
			ChestColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(25, 16, 7, 255),
				'EditableColor2', RGBA(31, 18, 2, 255),
				'EditableColor3', RGBA(177, 177, 177, 255),
			}),
			HairColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(15, 11, 8, 255),
			}),
			Hat = "",
			HatColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(9, 9, 9, 255),
				'EditableColor2', RGBA(3, 3, 3, 255),
				'EditableColor3', RGBA(40, 40, 40, 255),
			}),
			Head = "Head_M_IMP_01",
			HeadColor = PlaceObj('ColorizationPropSet', nil),
			Hip = "Faction_Acc_Artilery",
			HipColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(25, 16, 7, 255),
				'EditableColor2', RGBA(31, 18, 2, 255),
			}),
			Pants = "Faction_GrandChien_Bottom_02",
			PantsColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(60, 62, 60, 255),
				'EditableColor2', RGBA(225, 150, 53, 255),
				'EditableColor3', RGBA(64, 64, 64, 255),
			}),
			group = "Default",
			id = "APPID",
		}),
'@

$femaleApp = @'
		PlaceObj('ModItemAppearancePreset', {
			Armor = "",
			ArmorColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(0, 0, 0, 255),
				'EditableColor2', RGBA(0, 0, 0, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			Body = "EquipmentDrMangel_Top",
			BodyColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(0, 0, 0, 255),
				'EditableColor2', RGBA(14, 26, 20, 255),
				'EditableColor3', RGBA(14, 26, 20, 255),
			}),
			Chest = "",
			ChestColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(0, 0, 0, 255),
				'EditableColor2', RGBA(0, 0, 0, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			Hair = "NPCFemale_Hair_03",
			HairColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(42, 32, 21, 255),
				'EditableColor2', RGBA(35, 27, 18, 255),
				'EditableColor3', RGBA(32, 24, 16, 255),
			}),
			Hat = "",
			HatColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(220, 124, 0, 255),
				'EditableColor2', RGBA(220, 140, 28, 255),
				'EditableColor3', RGBA(154, 116, 73, 255),
			}),
			Head = "Head_F_Ca_NPC_07",
			HeadColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(0, 0, 0, 255),
				'EditableColor2', RGBA(0, 0, 0, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			Hip = "Faction_Acc_Soldier",
			HipColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(14, 26, 20, 255),
				'EditableColor2', RGBA(0, 0, 0, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			Pants = "EquipmentFemale_Pants_01",
			PantsColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(14, 26, 20, 255),
				'EditableColor2', RGBA(17, 19, 18, 255),
				'EditableColor3', RGBA(21, 26, 23, 255),
			}),
			Shirt = "",
			ShirtColor = PlaceObj('ColorizationPropSet', {
				'EditableColor1', RGBA(40, 64, 102, 255),
				'EditableColor2', RGBA(40, 64, 102, 255),
				'EditableColor3', RGBA(0, 0, 0, 255),
			}),
			group = "Default",
			id = "APPID",
		}),
'@

$unitFolders = New-Object System.Text.StringBuilder
$lootDefs = New-Object System.Text.StringBuilder
$appearances = New-Object System.Text.StringBuilder
$perkFolders = New-Object System.Text.StringBuilder
$metaUnits = New-Object System.Text.StringBuilder
$metaJazz = New-Object System.Text.StringBuilder

$itemsText = [IO.File]::ReadAllText((Join-Path $units 'items.lua'), [Text.Encoding]::UTF8)
$jitemsText = [IO.File]::ReadAllText((Join-Path $jazz 'items.lua'), [Text.Encoding]::UTF8)

foreach ($n in $missing) {
  $unitId = "Jazz_$n"
  $udPath = Join-Path $units "UnitData\$unitId.lua"
  $pkPath = Join-Path $jazz "CharacterEffect\Jazz_Perk_$n.lua"
  if (-not (Test-Path $udPath)) { throw "Missing $udPath" }
  $raw = [IO.File]::ReadAllText($udPath, [Text.Encoding]::UTF8)
  $body = ExtractDefineBody $udPath
  $fields = ConvertCompanionToModItemFields $body
  # bump indent: companion uses one tab, ModItem body uses 5 tabs under folder
  $fieldLines = ($fields -split "`r?`n") | ForEach-Object {
    if ($_ -eq '') { return $_ }
    # body starts with one tab from companion; we want 5 tabs for ModItem fields
    if ($_ -match '^\t') { return ("`t`t`t`t" + $_.TrimStart("`t")) }
    return ("`t`t`t`t" + $_)
  }
  $fieldsIndented = $fieldLines -join "`r`n"

  $gender = GetField $raw 'gender'
  if (-not $gender) { $gender = 'Male' }
  $nick = GetField $raw 'Nick'
  if (-not $nick) { $nick = $n }
  $preset = $n
  if ($raw -match "'Preset',\s*`"([^`"]+)`"") { $preset = $Matches[1] }
  $email = GetField $raw 'Email'
  $aff = 'AIM'
  if ($email -match '@merc\.com') { $aff = 'MERC' }

  # Affiliation if missing in fields
  if ($fieldsIndented -notmatch "'Affiliation'") {
    $fieldsIndented = "`t`t`t`t'Affiliation', `"$aff`",`r`n" + $fieldsIndented
  }

  $selId = $null
  if ($raw -match 'Selection[^\n]*T\((\d+)') { }
  # use Nick string for VR
  $vrNick = $nick -replace '^\[WIP\]\s*',''

  [void]$unitFolders.AppendLine("			PlaceObj('ModItemFolder', {")
  [void]$unitFolders.AppendLine("				'name', `"$unitId`",")
  [void]$unitFolders.AppendLine("			}, {")
  [void]$unitFolders.AppendLine("				PlaceObj('ModItemUnitDataCompositeDef', {")
  [void]$unitFolders.AppendLine("					'Group', `"MercenariesOld`",")
  [void]$unitFolders.AppendLine("					'Id', `"$unitId`",")
  [void]$unitFolders.AppendLine("					'object_class', `"UnitData`",")
  [void]$unitFolders.AppendLine($fieldsIndented)
  [void]$unitFolders.AppendLine("				}),")
  # VR: empty stub — FallbackMissingVR on UnitData covers combat lines
  [void]$unitFolders.AppendLine("				PlaceObj('ModItemVoiceResponse', {")
  [void]$unitFolders.AppendLine("					group = `"MercenariesOld`",")
  [void]$unitFolders.AppendLine("					id = `"$unitId`",")
  [void]$unitFolders.AppendLine("				}),")
  [void]$unitFolders.AppendLine("				}),")

  # Loot if missing
  $lootId = "Loot_JAZZ_$n"
  if ($itemsText -notmatch [regex]::Escape("id = `"$lootId`"")) {
    [void]$lootDefs.AppendLine("				PlaceObj('ModItemLootDef', {")
    [void]$lootDefs.AppendLine("					Comment = `"merc`",")
    [void]$lootDefs.AppendLine("					group = `"Mercs`",")
    [void]$lootDefs.AppendLine("					id = `"$lootId`",")
    [void]$lootDefs.AppendLine("					PlaceObj('LootEntryInventoryItem', {")
    [void]$lootDefs.AppendLine("						item = `"Knife`",")
    [void]$lootDefs.AppendLine("						stack_max = 1,")
    [void]$lootDefs.AppendLine("						stack_min = 1,")
    [void]$lootDefs.AppendLine("					}),")
    [void]$lootDefs.AppendLine("				}),")
  }

  # Appearance if missing
  if ($itemsText -notmatch [regex]::Escape("id = `"$preset`"")) {
    $app = if ($gender -eq 'Female') { $femaleApp } else { $maleApp }
    $app = $app.Replace('id = "APPID"', "id = `"$preset`"")
    [void]$appearances.AppendLine($app.TrimEnd())
  }

  # Perk ModItem
  $perkId = "Jazz_Perk_$n"
  $needPerk = $jitemsText -notmatch [regex]::Escape("'Id', `"$perkId`"")
  if ($needPerk -and (Test-Path $pkPath)) {
    $pk = [IO.File]::ReadAllText($pkPath, [Text.Encoding]::UTF8)
    $dnExpr = 'T("Perk")'; $ddExpr = 'T("WIP")'
    $icon = 'UI/Icons/Perks/MeleeTraining'
    if ($pk -match 'DisplayName = (T\([^\n]+)$') { $dnExpr = $Matches[1].Trim().TrimEnd(',') }
    if ($pk -match 'Description = (T\([^\n]+)$') { $ddExpr = $Matches[1].Trim().TrimEnd(',') }
    if ($pk -match 'Icon = `"([^`"]*)`"') { $icon = $Matches[1] }
    [void]$perkFolders.AppendLine("			PlaceObj('ModItemFolder', {")
    [void]$perkFolders.AppendLine("				'name', `"$n`",")
    [void]$perkFolders.AppendLine("			}, {")
    [void]$perkFolders.AppendLine("				PlaceObj('ModItemCharacterEffectCompositeDef', {")
    [void]$perkFolders.AppendLine("					'Group', `"Perk-Personal`",")
    [void]$perkFolders.AppendLine("					'Id', `"$perkId`",")
    [void]$perkFolders.AppendLine("					'object_class', `"Perk`",")
    [void]$perkFolders.AppendLine("					'unit_reactions', {},")
    [void]$perkFolders.AppendLine("					'DisplayName', $dnExpr,")
    [void]$perkFolders.AppendLine("					'Description', $ddExpr,")
    [void]$perkFolders.AppendLine("					'Icon', `"$icon`",")
    [void]$perkFolders.AppendLine("					'Tier', `"Personal`",")
    [void]$perkFolders.AppendLine("				}),")
    [void]$perkFolders.AppendLine("				}),")
  }

  [void]$metaUnits.AppendLine("		PlaceObj('ModResourcePreset', {")
  [void]$metaUnits.AppendLine("			'Class', `"UnitDataCompositeDef`",")
  [void]$metaUnits.AppendLine("			'Id', `"$unitId`",")
  [void]$metaUnits.AppendLine("			'ClassDisplayName', `"Unit`",")
  [void]$metaUnits.AppendLine("		}),")
  [void]$metaUnits.AppendLine("		PlaceObj('ModResourcePreset', {")
  [void]$metaUnits.AppendLine("			'Class', `"VoiceResponse`",")
  [void]$metaUnits.AppendLine("			'Id', `"$unitId`",")
  [void]$metaUnits.AppendLine("			'ClassDisplayName', `"Unit voice responses`",")
  [void]$metaUnits.AppendLine("		}),")
  [void]$metaUnits.AppendLine("		PlaceObj('ModResourcePreset', {")
  [void]$metaUnits.AppendLine("			'Class', `"AppearancePreset`",")
  [void]$metaUnits.AppendLine("			'Id', `"$preset`",")
  [void]$metaUnits.AppendLine("			'ClassDisplayName', `"Unit appearance`",")
  [void]$metaUnits.AppendLine("		}),")
  if ($itemsText -notmatch [regex]::Escape("id = `"$lootId`"")) {
    [void]$metaUnits.AppendLine("		PlaceObj('ModResourcePreset', {")
    [void]$metaUnits.AppendLine("			'Class', `"LootDef`",")
    [void]$metaUnits.AppendLine("			'Id', `"$lootId`",")
    [void]$metaUnits.AppendLine("			'ClassDisplayName', `"Loot definition`",")
    [void]$metaUnits.AppendLine("		}),")
  }
  [void]$metaJazz.AppendLine("		PlaceObj('ModResourcePreset', {")
  [void]$metaJazz.AppendLine("			'Class', `"CharacterEffectCompositeDef`",")
  [void]$metaJazz.AppendLine("			'Id', `"$perkId`",")
  [void]$metaJazz.AppendLine("			'ClassDisplayName', `"Character effect`",")
  [void]$metaJazz.AppendLine("		}),")
}

Write-Host "Building inserts..."

# --- Patch jazz-units items.lua ---
$uPath = Join-Path $units 'items.lua'
$u = [IO.File]::ReadAllText($uPath, [Text.Encoding]::UTF8)
$anchor = "			PlaceObj('ModItemFolder', {`r`n				'name', `"Merc_Spouke`","
if ($u -notmatch [regex]::Escape("Merc_Spouke")) { throw 'Merc_Spouke anchor missing' }
# normalize newline
if ($u.Contains("			PlaceObj('ModItemFolder', {`n				'name', `"Merc_Spouke`"")) {
  $anchor = "			PlaceObj('ModItemFolder', {`n				'name', `"Merc_Spouke`","
}
$insertFolders = $unitFolders.ToString().TrimEnd() + "`r`n"
if ($u -match "'name', `"Jazz_Bull`"") { Write-Host 'WARN: Jazz_Bull already in items' }
else {
  $u = $u.Replace($anchor, $insertFolders + $anchor)
  Write-Host "Inserted $($missing.Count) unit folders before Merc_Spouke"
}

# Loot after Loot_JAZZ_Grom block (compact one-liner entries)
if ($lootDefs.Length -gt 0) {
  $m = [regex]::Match($u, '(?s)PlaceObj\(''ModItemLootDef'', \{\s*Comment = "merc",\s*group = "Mercs",\s*id = "Loot_JAZZ_Grom",.*?\}\),')
  if (-not $m.Success) { throw 'Cannot find Loot_JAZZ_Grom block' }
  $u = $u.Insert($m.Index + $m.Length, "`r`n" + $lootDefs.ToString())
  Write-Host "Inserted loot defs"
}

# Appearances after Ira appearance (id = "Ira")
if ($appearances.Length -gt 0) {
  $m = [regex]::Match($u, '(?s)\t\tPlaceObj\(''ModItemAppearancePreset'', \{.*?id = "Ira",\s*\}\),')
  if (-not $m.Success) { throw 'Ira appearance anchor missing' }
  $u = $u.Insert($m.Index + $m.Length, "`r`n" + $appearances.ToString())
  Write-Host "Inserted appearances"
}

[IO.File]::WriteAllText($uPath, $u, $utf8)

# --- Patch jazz items.lua perks ---
$jPath = Join-Path $jazz 'items.lua'
$j = [IO.File]::ReadAllText($jPath, [Text.Encoding]::UTF8)
if ($perkFolders.Length -gt 0) {
  # insert after Grom perk folder
  $pm = [regex]::Match($j, "(?s)PlaceObj\('ModItemFolder', \{\s*'name', `"Grom`",\s*\}, \{\s*PlaceObj\('ModItemCharacterEffectCompositeDef', \{.*?\}\),\s*\}\),")
  if (-not $pm.Success) { throw 'Grom perk folder anchor missing' }
  $j = $j.Insert($pm.Index + $pm.Length, "`r`n" + $perkFolders.ToString())
  [IO.File]::WriteAllText($jPath, $j, $utf8)
  Write-Host "Inserted perk folders"
}

# --- metadata units ---
$umPath = Join-Path $units 'metadata.lua'
$um = [IO.File]::ReadAllText($umPath, [Text.Encoding]::UTF8)
# insert before closing of affected_resources - after last AppearancePreset Jazz_Grom if any, else before final `},` of affected_resources
# Safer: append before the last `	},` that closes affected_resources - find Jazz_Grom UnitDataCompositeDef and insert after VR Grom block
$gm = [regex]::Match($um, "(?s)PlaceObj\('ModResourcePreset', \{\s*'Class', `"VoiceResponse`",\s*'Id', `"Jazz_Grom`",\s*'ClassDisplayName', `"Unit voice responses`",\s*\}\),")
if ($gm.Success) {
  $um = $um.Insert($gm.Index + $gm.Length, "`r`n" + $metaUnits.ToString())
} else {
  throw 'Jazz_Grom VR meta anchor missing'
}
[IO.File]::WriteAllText($umPath, $um, $utf8)
Write-Host "Patched units metadata"

# --- metadata jazz ---
$jmPath = Join-Path $jazz 'metadata.lua'
$jm = [IO.File]::ReadAllText($jmPath, [Text.Encoding]::UTF8)
$gpm = [regex]::Match($jm, "(?s)PlaceObj\('ModResourcePreset', \{\s*'Class', `"CharacterEffectCompositeDef`",\s*'Id', `"Jazz_Perk_Grom`",.*?\}$\s*\),", [System.Text.RegularExpressions.RegexOptions]::Multiline)
if (-not $gpm.Success) {
  $gpm = [regex]::Match($jm, "PlaceObj\('ModResourcePreset', \{\s*'Class', `"CharacterEffectCompositeDef`",\s*'Id', `"Jazz_Perk_Grom`",\s*'ClassDisplayName', `"Character effect`",\s*\}\),")
}
if (-not $gpm.Success) { throw 'Jazz_Perk_Grom meta missing' }
$jm = $jm.Insert($gpm.Index + $gpm.Length, "`r`n" + $metaJazz.ToString())
[IO.File]::WriteAllText($jmPath, $jm, $utf8)
Write-Host "Patched jazz metadata"

# Verify
$u2 = [IO.File]::ReadAllText($uPath, [Text.Encoding]::UTF8)
$ok = 0
foreach ($n in $missing) {
  if ($u2 -match [regex]::Escape("'Id', `"Jazz_$n`"")) { $ok++ } else { Write-Host "MISSING items Id Jazz_$n" }
}
Write-Host "Unit ModItems present: $ok / $($missing.Count)"
Write-Host 'Done.'
