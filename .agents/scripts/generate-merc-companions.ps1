# Generate minimal UnitData + Perk companions from executable merc articles
param(
  [string[]]$Slugs
)
$ErrorActionPreference = 'Stop'
$jazz = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz'
$units = 'C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units'
$base = Join-Path $jazz 'docs\design\mercs-ja12'
$locStart = 890000000002100L
$idFile = Join-Path $base '_loc-id-cursor.txt'
if (Test-Path $idFile) { $locStart = [int64](Get-Content $idFile -Raw).Trim() }
function NextId { $script:locStart++; return $script:locStart }
function GetFm([string]$text, [string]$key) {
  if ($text -match "(?m)^${key}:\s*(.+)$") { return $Matches[1].Trim() }
  return ''
}
function GetStat([string]$text, [string]$stat) {
  if ($text -match "(?m)\|\s*$stat\s*\|\s*(\d+)\s*\|") { return [int]$Matches[1] }
  return 50
}
function Ident([string]$text, [string]$field, [string]$lang) {
  # table row: | Field | RU | EN |
  if ($text -match "(?m)\|\s*$field\s*\|\s*([^|]+)\|\s*([^|]+)\|") {
    if ($lang -eq 'EN') { return $Matches[2].Trim() }
    return $Matches[1].Trim()
  }
  return $field
}

if (-not $Slugs -or $Slugs.Count -eq 0) {
  $Slugs = Get-ChildItem $base -Filter '*.md' | Where-Object { $_.Name -notmatch '^_' } | ForEach-Object { $_.BaseName }
}

$ruAdd = New-Object System.Collections.Generic.List[string]
$enAdd = New-Object System.Collections.Generic.List[string]
$metaUnits = [IO.File]::ReadAllText((Join-Path $units 'metadata.lua'))
$metaJazz = [IO.File]::ReadAllText((Join-Path $jazz 'metadata.lua'))

foreach ($slug in $Slugs) {
  $art = Join-Path $base "$slug.md"
  if (-not (Test-Path $art)) { continue }
  $text = Get-Content $art -Raw
  if ($text -notmatch '(?m)^executable:\s*true') { Write-Host "skip $slug not exec"; continue }
  $unitId = GetFm $text 'unit_id'
  $portraitId = GetFm $text 'portrait_id'
  if (-not $unitId) { continue }
  $udPath = Join-Path $units "UnitData\$unitId.lua"
  $perkId = "Jazz_Perk_$portraitId"
  $perkPath = Join-Path $jazz "CharacterEffect\$perkId.lua"
  if ((Test-Path $udPath) -and (Test-Path $perkPath)) { Write-Host "have $slug"; continue }

  $nameRu = Ident $text 'Name' 'RU'
  $nameEn = Ident $text 'Name' 'EN'
  $nickRu = Ident $text 'Nick' 'RU'
  $nickEn = Ident $text 'Nick' 'EN'
  $capsRu = Ident $text 'AllCapsNick' 'RU'
  $capsEn = Ident $text 'AllCapsNick' 'EN'
  $titleRu = Ident $text 'Title' 'RU'
  $titleEn = Ident $text 'Title' 'EN'
  $email = Ident $text 'Email' 'EN'
  $snype = Ident $text 'snype_nick' 'EN'
  $nat = GetFm $text 'nationality'
  $gender = GetFm $text 'gender'
  $spec = GetFm $text 'specialization'
  $tier = GetFm $text 'tier'
  $will = GetFm $text 'will'
  $lvl = GetFm $text 'starting_level'
  if (-not $lvl) { $lvl = '3' }
  # salary from yaml block - rough
  $salStart = 1000; $salInc = 100; $sal1 = 400; $salMax = 3000
  if ($text -match '(?ms)^salary:\s*\r?\n(?:\s+\w+:\s*.+\r?\n)+') {
    $sb = $Matches[0]
    if ($sb -match 'starting:\s*(\d+)') { $salStart = [int]$Matches[1] }
    if ($sb -match 'increase:\s*(\d+)') { $salInc = [int]$Matches[1] }
    if ($sb -match 'lv1:\s*(\d+)') { $sal1 = [int]$Matches[1] }
    if ($sb -match 'max:\s*(\d+)') { $salMax = [int]$Matches[1] }
  }
  $med = GetFm $text 'medical_deposit'
  if (-not $med) { $med = 'large' }
  $fallback = 'Ice'
  if ($text -match 'FallbackMissingVR\s*\|\s*(\w+)') { $fallback = $Matches[1] }

  # perk name from table
  $perkNameRu = "$nickRu"
  $perkNameEn = "$nickEn"
  $perkDescRu = "Именной перк $nickRu"
  $perkDescEn = "Named perk $nickEn"
  if ($text -match '(?ms)DisplayName RU/EN\s*\|\s*([^/]+)/\s*([^\|]+)\|') {
    $perkNameRu = $Matches[1].Trim(); $perkNameEn = $Matches[2].Trim()
  }
  if ($text -match '(?ms)Description RU/EN\s*\|\s*([^/]+)/\s*([^\|]+)\|') {
    $perkDescRu = $Matches[1].Trim(); $perkDescEn = $Matches[2].Trim()
  }

  $idName = NextId; $idNick = NextId; $idCaps = NextId; $idBio = NextId; $idTitle = NextId
  $idEmail = NextId; $idSnype = NextId
  $idOff = NextId; $idGreet = NextId; $idRest = NextId; $idIdle = NextId; $idPart = NextId; $idRehI = NextId; $idRehO = NextId
  $idPerkN = NextId; $idPerkD = NextId

  $bioRu = "Наёмник $nameRu."
  $bioEn = "Mercenary $nameEn."
  if ($text -match '(?ms)\*\*RU:\*\*\s*(.+?)\r?\n\r?\n\*\*EN:\*\*') { $bioRu = $Matches[1].Trim() -replace '\r?\n',' ' }
  if ($text -match '(?ms)\*\*EN:\*\*\s*(.+?)\r?\n\r?\n## ') { $bioEn = $Matches[1].Trim() -replace '\r?\n',' ' }

  $H = GetStat $text 'Health'; $A = GetStat $text 'Agility'; $D = GetStat $text 'Dexterity'
  $S = GetStat $text 'Strength'; $W = GetStat $text 'Wisdom'; $Wi = if ($will) {[int]$will} else { GetStat $text 'Will' }
  $L = GetStat $text 'Leadership'; $M = GetStat $text 'Marksmanship'
  $Mech = GetStat $text 'Mechanical'; $E = GetStat $text 'Explosives'; $MedS = GetStat $text 'Medical'
  $MHP = GetStat $text 'MaxHitPoints'; if ($MHP -eq 50) { $MHP = $H }

  $polly = if ($gender -eq 'Female') { 'Amy' } else { 'Matthew' }
  $loot = "Loot_JAZZ_$portraitId"

  # StartingPerks from article bullets with backticks
  $perks = @($perkId)
  [regex]::Matches($text, '(?m)^-\s*`([^`]+)`') | ForEach-Object {
    $p = $_.Groups[1].Value
    if ($p -notmatch '^Loot_' -and $p -notmatch '^Jazz_Perk_' -and $perks -notcontains $p -and $p -notmatch ' ') { $perks += $p }
  }
  if ($perks -notcontains $perkId) { $perks = @($perkId) + $perks }

  function Esc([string]$s) { return ($s -replace '\\','\\' -replace '"','\"') }
  function Csv([string]$s) {
    if ($s -match '[",\r\n]') { return '"' + ($s -replace '"','""') + '"' }
    return $s
  }

  $perkLua = @"
UndefineClass('$perkId')
DefineClass.$perkId = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T($idPerkN, --[[ModItemCharacterEffectCompositeDef $perkId DisplayName]] "$(Esc $perkNameRu)"),
	Description = T($idPerkD, --[[ModItemCharacterEffectCompositeDef $perkId Description]] "$(Esc $perkDescRu)"),
	Icon = "UI/Icons/Perks/Thinking",
	Tier = "Personal",
}
"@
  Set-Content -Path $perkPath -Value $perkLua -Encoding utf8

  $perkList = ($perks | ForEach-Object { "`t`t`"$_`"," }) -join "`n"
  $udLua = @"
UndefineClass('$unitId')
DefineClass.$unitId = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",


	object_class = "UnitData",
	Health = $H,
	Agility = $A,
	Dexterity = $D,
	Strength = $S,
	Wisdom = $W,
	Will = $Wi,
	Leadership = $L,
	Marksmanship = $M,
	Mechanical = $Mech,
	Explosives = $E,
	Medical = $MedS,
	Portrait = "Mod/Dv3mFVN/MercPortraits/$portraitId.png",
	BigPortrait = "Mod/Dv3mFVN/MercPortraits/${portraitId}_Big.png",
	IsMercenary = true,
	Name = T($idName, --[[ModItemUnitDataCompositeDef $unitId Name]] "$(Esc $nameRu)"),
	Nick = T($idNick, --[[ModItemUnitDataCompositeDef $unitId Nick]] "$(Esc $nickRu)"),
	AllCapsNick = T($idCaps, --[[ModItemUnitDataCompositeDef $unitId AllCapsNick]] "$(Esc $capsRu)"),
	Bio = T($idBio, --[[ModItemUnitDataCompositeDef $unitId Bio]] "$(Esc $bioRu)"),
	Nationality = "$nat",
	Title = T($idTitle, --[[ModItemUnitDataCompositeDef $unitId Title]] "$(Esc $titleRu)"),
	Email = T($idEmail, --[[ModItemUnitDataCompositeDef $unitId Email]] "$(Esc $email)"),
	snype_nick = T($idSnype, --[[ModItemUnitDataCompositeDef $unitId snype_nick]] "$(Esc $snype)"),
	Offline = {
		PlaceObj('ChatMessage', {
			'Text', T($idOff, --[[ModItemUnitDataCompositeDef $unitId Text Offline ChatMessage voice:$unitId]] "$(Esc $nickRu). Offline."),
		}),
	},
	GreetingAndOffer = {
		PlaceObj('ChatMessage', {
			'Text', T($idGreet, --[[ModItemUnitDataCompositeDef $unitId Text GreetingAndOffer ChatMessage voice:$unitId]] "$(Esc $nickRu) online."),
		}),
	},
	ConversationRestart = {
		PlaceObj('ChatMessage', {
			'Text', T($idRest, --[[ModItemUnitDataCompositeDef $unitId Text ConversationRestart ChatMessage voice:$unitId]] "Continue."),
		}),
	},
	IdleLine = {
		PlaceObj('ChatMessage', {
			'Text', T($idIdle, --[[ModItemUnitDataCompositeDef $unitId Text IdleLine ChatMessage voice:$unitId]] "Waiting."),
		}),
	},
	PartingWords = {
		PlaceObj('ChatMessage', {
			'Text', T($idPart, --[[ModItemUnitDataCompositeDef $unitId Text PartingWords ChatMessage voice:$unitId]] "Hired."),
		}),
	},
	RehireIntro = {
		PlaceObj('ChatMessage', {
			'Text', T($idRehI, --[[ModItemUnitDataCompositeDef $unitId Text RehireIntro ChatMessage voice:$unitId]] "Contract ending?"),
		}),
	},
	RehireOutro = {
		PlaceObj('ChatMessage', {
			'Text', T($idRehO, --[[ModItemUnitDataCompositeDef $unitId Text RehireOutro ChatMessage voice:$unitId]] "Staying."),
		}),
	},
	MedicalDeposit = "$med",
	StartingSalary = $salStart,
	SalaryIncrease = $salInc,
	SalaryLv1 = $sal1,
	SalaryMaxLv = $salMax,
	StartingLevel = $lvl,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = $MHP,
	StartingPerks = {
$perkList
	},
	AppearancesList = {
		PlaceObj('AppearanceWeight', {
			'Preset', "$portraitId",
		}),
	},
	Equipment = {
		"$loot",
	},
	Tier = "$tier",
	Specialization = "$spec",
	pollyvoice = "$polly",
	gender = "$gender",
	VoiceResponseId = "$unitId",
	FallbackMissingVR = "$fallback",
	DaysUntilOnline = 0,
}
"@
  Set-Content -Path $udPath -Value $udLua -Encoding utf8

  # loc rows
  $pairs = @(
    @{id=$idPerkN; ru=$perkNameRu; en=$perkNameEn},
    @{id=$idPerkD; ru=$perkDescRu; en=$perkDescEn},
    @{id=$idName; ru=$nameRu; en=$nameEn},
    @{id=$idNick; ru=$nickRu; en=$nickEn},
    @{id=$idCaps; ru=$capsRu; en=$capsEn},
    @{id=$idBio; ru=$bioRu; en=$bioEn},
    @{id=$idTitle; ru=$titleRu; en=$titleEn},
    @{id=$idEmail; ru=$email; en=$email},
    @{id=$idSnype; ru=$snype; en=$snype},
    @{id=$idOff; ru="$nickRu. Offline."; en="$nickEn. Offline."},
    @{id=$idGreet; ru="$nickRu online."; en="$nickEn online."},
    @{id=$idRest; ru='Продолжаем.'; en='Continue.'},
    @{id=$idIdle; ru='Жду.'; en='Waiting.'},
    @{id=$idPart; ru='Нанят.'; en='Hired.'},
    @{id=$idRehI; ru='Контракт кончается?'; en='Contract ending?'},
    @{id=$idRehO; ru='Остаюсь.'; en='Staying.'}
  )
  foreach ($p in $pairs) {
    $ruAdd.Add("$($p.id),$(Csv $p.ru),$(Csv $p.ru),,$unitId")
    $enAdd.Add("$($p.id),$(Csv $p.en),$(Csv $p.en),,$unitId")
  }

  # metadata
  if ($metaUnits -notmatch [regex]::Escape("UnitData/$unitId.lua")) {
    $metaUnits = $metaUnits -replace '("UnitData/Jazz_Grom.lua",)', "`$1`r`n`t`t`"UnitData/$unitId.lua`","
  }
  if ($metaJazz -notmatch [regex]::Escape("CharacterEffect/$perkId.lua")) {
    $metaJazz = $metaJazz -replace '("CharacterEffect/Jazz_Perk_Grom.lua",)', "`$1`r`n`t`t`"CharacterEffect/$perkId.lua`","
  }

  # minimal loot parent if missing
  $itemsPath = Join-Path $units 'items.lua'
  $items = [IO.File]::ReadAllText($itemsPath)
  if ($items -notmatch [regex]::Escape("id = `"$loot`"")) {
    $lootBlock = @"

				PlaceObj('ModItemLootDef', {
					Comment = "merc",
					group = "Mercs",
					id = "$loot",
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}50", weight = 50000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}35", weight = 35000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}25", weight = 25000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}20", weight = 20000 }),
				}),
				PlaceObj('ModItemLootDef', {
					Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}50", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
					PlaceObj('LootEntryInventoryItem', { item = "Meds", stack_max = 10, stack_min = 10 }),
				}),
				PlaceObj('ModItemLootDef', {
					Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}35", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
				PlaceObj('ModItemLootDef', {
					Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}25", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
				PlaceObj('ModItemLootDef', {
					Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}20", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
"@
    $ins = $items.IndexOf('id = "Loot_JAZZ_Grom"')
    if ($ins -lt 0) { $ins = $items.IndexOf('id = "Loot_JAZZ_Colby"') }
    if ($ins -gt 0) {
      $end = $items.IndexOf('}),', $items.IndexOf('weight = 20000', $ins)) + 3
      $items = $items.Insert($end, $lootBlock)
      [IO.File]::WriteAllText($itemsPath, $items)
    }
  }

  Write-Host "generated $slug -> $unitId / $perkId"
}

[IO.File]::WriteAllText((Join-Path $units 'metadata.lua'), $metaUnits)
[IO.File]::WriteAllText((Join-Path $jazz 'metadata.lua'), $metaJazz)
if ($ruAdd.Count -gt 0) {
  Add-Content (Join-Path $jazz 'Russian.csv') ($ruAdd -join "`n") -Encoding UTF8
  Add-Content (Join-Path $jazz 'English.csv') ($enAdd -join "`n") -Encoding UTF8
}
Set-Content $idFile -Value $locStart -Encoding ascii
Write-Host "DONE locCursor=$locStart addedLoc=$($ruAdd.Count)"
