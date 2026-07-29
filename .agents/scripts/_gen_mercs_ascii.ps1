# Patch: regenerate companions ASCII-safe
$ErrorActionPreference = "Stop"
$jazz = "C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz"
$units = "C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units"
$base = Join-Path $jazz "docs\design\mercs-ja12"
$locStart = 890000000002100L
$idFile = Join-Path $base "_loc-id-cursor.txt"
if (Test-Path $idFile) { $locStart = [int64](Get-Content $idFile -Raw).Trim() }
function NextId { $script:locStart++; return $script:locStart }
function GetFm($text,$key){ if($text -match "(?m)^${key}:\s*(.+)$"){return $Matches[1].Trim()}; "" }
function GetStat($text,$stat){ if($text -match "(?m)\|\s*$stat\s*\|\s*(\d+)\s*\|"){return [int]$Matches[1]}; 50 }
function Ident($text,$field,$lang){
  if($text -match "(?m)\|\s*$field\s*\|\s*([^|]+)\|\s*([^|]+)\|"){
    if($lang -eq "EN"){return $Matches[2].Trim()}; return $Matches[1].Trim()
  }; return $field
}
function Esc($s){ if($null -eq $s){return ""}; return ($s -replace "\\","\\" -replace "`"","\`"") }
function Csv($s){ if($null -eq $s){return ""}; if($s -match "[`",\r\n]"){ return "`"" + ($s -replace "`"","`"`"") + "`"" }; return $s }

$slugs = @(
 "rothman","quinten","vicious","biff","nervous","flo","cougar","miguel","gamos","dynamo","gaston","horg","manuel","monk","allik","henning",
 "static","highball","bull","cord","hobbit","ricochet","meat","carlos","devin","shank","vince","hitman","biggens","kulba","vilde","grace","steiger","lucky","laura","eskimo"
)
$ruAdd = New-Object System.Collections.Generic.List[string]
$enAdd = New-Object System.Collections.Generic.List[string]
$metaUnits = [IO.File]::ReadAllText((Join-Path $units "metadata.lua"))
$metaJazz = [IO.File]::ReadAllText((Join-Path $jazz "metadata.lua"))
$itemsPath = Join-Path $units "items.lua"
$items = [IO.File]::ReadAllText($itemsPath)

foreach($slug in $slugs){
  $art = Join-Path $base "$slug.md"
  if(-not (Test-Path $art)){ continue }
  $text = Get-Content $art -Raw -Encoding UTF8
  if($text -notmatch "(?m)^executable:\s*true"){ Write-Host "skip $slug"; continue }
  $unitId = GetFm $text "unit_id"; $portraitId = GetFm $text "portrait_id"
  if(-not $unitId){ continue }
  $udPath = Join-Path $units "UnitData\$unitId.lua"
  $perkId = "Jazz_Perk_$portraitId"
  $perkPath = Join-Path $jazz "CharacterEffect\$perkId.lua"
  if((Test-Path $udPath) -and (Test-Path $perkPath)){ Write-Host "have $slug"; continue }

  $nameRu = Ident $text "Name" "RU"; $nameEn = Ident $text "Name" "EN"
  $nickRu = Ident $text "Nick" "RU"; $nickEn = Ident $text "Nick" "EN"
  $capsRu = Ident $text "AllCapsNick" "RU"; $capsEn = Ident $text "AllCapsNick" "EN"
  $titleRu = Ident $text "Title" "RU"; $titleEn = Ident $text "Title" "EN"
  $email = Ident $text "Email" "EN"; $snype = Ident $text "snype_nick" "EN"
  $nat = GetFm $text "nationality"; $gender = GetFm $text "gender"
  $spec = GetFm $text "specialization"; $tier = GetFm $text "tier"
  $will = GetFm $text "will"; $lvl = GetFm $text "starting_level"; if(-not $lvl){$lvl="3"}
  $salStart=1000;$salInc=100;$sal1=400;$salMax=3000
  if($text -match "(?ms)^salary:\s*\r?\n(?:\s+\w+:\s*.+\r?\n)+"){
    $sb=$Matches[0]
    if($sb -match "starting:\s*(\d+)"){$salStart=[int]$Matches[1]}
    if($sb -match "increase:\s*(\d+)"){$salInc=[int]$Matches[1]}
    if($sb -match "lv1:\s*(\d+)"){$sal1=[int]$Matches[1]}
    if($sb -match "max:\s*(\d+)"){$salMax=[int]$Matches[1]}
  }
  $med = GetFm $text "medical_deposit"; if(-not $med){$med="large"}
  $fallback="Ice"; if($text -match "FallbackMissingVR\s*\|\s*(\w+)"){$fallback=$Matches[1]}
  $perkNameRu=$nickRu; $perkNameEn=$nickEn; $perkDescRu="Named perk"; $perkDescEn="Named perk"
  if($text -match "(?ms)DisplayName RU/EN\s*\|\s*([^/]+)/\s*([^\|]+)\|"){ $perkNameRu=$Matches[1].Trim(); $perkNameEn=$Matches[2].Trim() }
  if($text -match "(?ms)Description RU/EN\s*\|\s*([^/]+)/\s*([^\|]+)\|"){ $perkDescRu=$Matches[1].Trim(); $perkDescEn=$Matches[2].Trim() }
  $bioRu = "Merc $nameRu."; $bioEn = "Merc $nameEn."
  if($text -match "(?ms)\*\*RU:\*\*\s*(.+?)\r?\n\r?\n\*\*EN:\*\*"){ $bioRu = ($Matches[1].Trim() -replace "\r?\n"," ") }
  if($text -match "(?ms)\*\*EN:\*\*\s*(.+?)\r?\n\r?\n## "){ $bioEn = ($Matches[1].Trim() -replace "\r?\n"," ") }

  $ids = @{}; foreach($k in @("perkN","perkD","name","nick","caps","bio","title","email","snype","off","greet","rest","idle","part","rehi","reho")){ $ids[$k]=NextId }

  $H=GetStat $text "Health"; $A=GetStat $text "Agility"; $D=GetStat $text "Dexterity"; $S=GetStat $text "Strength"
  $W=GetStat $text "Wisdom"; $Wi= if($will){[int]$will}else{GetStat $text "Will"}
  $L=GetStat $text "Leadership"; $M=GetStat $text "Marksmanship"; $Mech=GetStat $text "Mechanical"
  $E=GetStat $text "Explosives"; $MedS=GetStat $text "Medical"; $MHP=GetStat $text "MaxHitPoints"; if($MHP -eq 50){$MHP=$H}
  $polly = if($gender -eq "Female"){"Amy"}else{"Matthew"}
  $loot = "Loot_JAZZ_$portraitId"
  $perks = @($perkId)
  [regex]::Matches($text,"(?m)^-\s*`([^`]+)`") | ForEach-Object {
    $p=$_.Groups[1].Value
    if($p -notmatch "^Loot_|Jazz_Perk_| " -and $perks -notcontains $p){ $perks += $p }
  }

  $perkLua = @"
UndefineClass('$perkId')
DefineClass.$perkId = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T($($ids.perkN), --[[ModItemCharacterEffectCompositeDef $perkId DisplayName]] "$(Esc $perkNameRu)"),
	Description = T($($ids.perkD), --[[ModItemCharacterEffectCompositeDef $perkId Description]] "$(Esc $perkDescRu)"),
	Icon = "UI/Icons/Perks/Thinking",
	Tier = "Personal",
}
"@
  [IO.File]::WriteAllText($perkPath, $perkLua, [Text.UTF8Encoding]::new($false))

  $perkList = ($perks | ForEach-Object { "`t`t`"$_`"," }) -join "`n"
  $udLua = @"
UndefineClass('$unitId')
DefineClass.$unitId = {
	__parents = { "UnitData" },
	__generated_by_class = "ModItemUnitDataCompositeDef",
	object_class = "UnitData",
	Health = $H, Agility = $A, Dexterity = $D, Strength = $S, Wisdom = $W, Will = $Wi,
	Leadership = $L, Marksmanship = $M, Mechanical = $Mech, Explosives = $E, Medical = $MedS,
	Portrait = "Mod/Dv3mFVN/MercPortraits/$portraitId.png",
	BigPortrait = "Mod/Dv3mFVN/MercPortraits/${portraitId}_Big.png",
	IsMercenary = true,
	Name = T($($ids.name), --[[ModItemUnitDataCompositeDef $unitId Name]] "$(Esc $nameRu)"),
	Nick = T($($ids.nick), --[[ModItemUnitDataCompositeDef $unitId Nick]] "$(Esc $nickRu)"),
	AllCapsNick = T($($ids.caps), --[[ModItemUnitDataCompositeDef $unitId AllCapsNick]] "$(Esc $capsRu)"),
	Bio = T($($ids.bio), --[[ModItemUnitDataCompositeDef $unitId Bio]] "$(Esc $bioRu)"),
	Nationality = "$nat",
	Title = T($($ids.title), --[[ModItemUnitDataCompositeDef $unitId Title]] "$(Esc $titleRu)"),
	Email = T($($ids.email), --[[ModItemUnitDataCompositeDef $unitId Email]] "$(Esc $email)"),
	snype_nick = T($($ids.snype), --[[ModItemUnitDataCompositeDef $unitId snype_nick]] "$(Esc $snype)"),
	Offline = { PlaceObj('ChatMessage', { 'Text', T($($ids.off), --[[voice:$unitId]] "$(Esc $nickEn) offline.") }) },
	GreetingAndOffer = { PlaceObj('ChatMessage', { 'Text', T($($ids.greet), --[[voice:$unitId]] "$(Esc $nickEn) here.") }) },
	ConversationRestart = { PlaceObj('ChatMessage', { 'Text', T($($ids.rest), --[[voice:$unitId]] "Continue.") }) },
	IdleLine = { PlaceObj('ChatMessage', { 'Text', T($($ids.idle), --[[voice:$unitId]] "Waiting.") }) },
	PartingWords = { PlaceObj('ChatMessage', { 'Text', T($($ids.part), --[[voice:$unitId]] "Hired.") }) },
	RehireIntro = { PlaceObj('ChatMessage', { 'Text', T($($ids.rehi), --[[voice:$unitId]] "Contract ending?") }) },
	RehireOutro = { PlaceObj('ChatMessage', { 'Text', T($($ids.reho), --[[voice:$unitId]] "Staying.") }) },
	MedicalDeposit = "$med",
	StartingSalary = $salStart, SalaryIncrease = $salInc, SalaryLv1 = $sal1, SalaryMaxLv = $salMax,
	StartingLevel = $lvl,
	CustomEquipGear = function (self, items)
		self:TryEquip(items, "Handheld A", "Firearm")
		self:TryEquip(items, "Handheld B", "Firearm")
	end,
	MaxHitPoints = $MHP,
	StartingPerks = {
$perkList
	},
	AppearancesList = { PlaceObj('AppearanceWeight', { 'Preset', "$portraitId" }) },
	Equipment = { "$loot" },
	Tier = "$tier", Specialization = "$spec", pollyvoice = "$polly", gender = "$gender",
	VoiceResponseId = "$unitId", FallbackMissingVR = "$fallback", DaysUntilOnline = 0,
}
"@
  [IO.File]::WriteAllText($udPath, $udLua, [Text.UTF8Encoding]::new($false))

  $locPairs = @(
    @{id=$ids.perkN;ru=$perkNameRu;en=$perkNameEn}, @{id=$ids.perkD;ru=$perkDescRu;en=$perkDescEn},
    @{id=$ids.name;ru=$nameRu;en=$nameEn}, @{id=$ids.nick;ru=$nickRu;en=$nickEn},
    @{id=$ids.caps;ru=$capsRu;en=$capsEn}, @{id=$ids.bio;ru=$bioRu;en=$bioEn},
    @{id=$ids.title;ru=$titleRu;en=$titleEn}, @{id=$ids.email;ru=$email;en=$email},
    @{id=$ids.snype;ru=$snype;en=$snype},
    @{id=$ids.off;ru="$nickEn offline.";en="$nickEn offline."},
    @{id=$ids.greet;ru="$nickEn here.";en="$nickEn here."},
    @{id=$ids.rest;ru="Continue.";en="Continue."}, @{id=$ids.idle;ru="Waiting.";en="Waiting."},
    @{id=$ids.part;ru="Hired.";en="Hired."}, @{id=$ids.rehi;ru="Contract ending?";en="Contract ending?"},
    @{id=$ids.reho;ru="Staying.";en="Staying."}
  )
  foreach($p in $locPairs){
    $ruAdd.Add("$($p.id),$(Csv $p.ru),$(Csv $p.ru),,$unitId")
    $enAdd.Add("$($p.id),$(Csv $p.en),$(Csv $p.en),,$unitId")
  }

  if($metaUnits -notmatch [regex]::Escape("UnitData/$unitId.lua")){
    $metaUnits = $metaUnits.Replace("`t`t`"UnitData/Jazz_Grom.lua`",", "`t`t`"UnitData/Jazz_Grom.lua`",`r`n`t`t`"UnitData/$unitId.lua`",")
  }
  if($metaJazz -notmatch [regex]::Escape("CharacterEffect/$perkId.lua")){
    $metaJazz = $metaJazz.Replace("`t`t`"CharacterEffect/Jazz_Perk_Grom.lua`",", "`t`t`"CharacterEffect/Jazz_Perk_Grom.lua`",`r`n`t`t`"CharacterEffect/$perkId.lua`",")
  }

  if($items -notmatch [regex]::Escape("id = `"$loot`"")){
    $lootBlock = @"

				PlaceObj('ModItemLootDef', {
					Comment = "merc", group = "Mercs", id = "$loot",
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}50", weight = 50000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}35", weight = 35000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}25", weight = 25000 }),
					PlaceObj('LootEntryLootDef', { loot_def = "JAZZ_${portraitId}20", weight = 20000 }),
				}),
				PlaceObj('ModItemLootDef', { Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}50", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
				PlaceObj('ModItemLootDef', { Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}35", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
				PlaceObj('ModItemLootDef', { Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}25", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
				PlaceObj('ModItemLootDef', { Comment = "merc", group = "Mercs", id = "JAZZ_${portraitId}20", loot = "all",
					PlaceObj('LootEntryInventoryItem', { item = "Knife", stack_max = 1, stack_min = 1 }),
				}),
"@
    $marker = 'id = "Loot_JAZZ_Grom"'
    $ins = $items.IndexOf($marker)
    if($ins -lt 0){ $ins = $items.IndexOf('id = "Loot_JAZZ_Colby"') }
    if($ins -gt 0){
      $w = $items.IndexOf('weight = 20000', $ins)
      $end = $items.IndexOf('}),', $w) + 3
      $items = $items.Insert($end, $lootBlock)
    }
  }
  Write-Host "generated $slug"
}

[IO.File]::WriteAllText((Join-Path $units "metadata.lua"), $metaUnits)
[IO.File]::WriteAllText((Join-Path $jazz "metadata.lua"), $metaJazz)
[IO.File]::WriteAllText($itemsPath, $items)
if($ruAdd.Count -gt 0){
  Add-Content (Join-Path $jazz "Russian.csv") ($ruAdd -join "`n") -Encoding UTF8
  Add-Content (Join-Path $jazz "English.csv") ($enAdd -join "`n") -Encoding UTF8
}
Set-Content $idFile -Value $locStart -Encoding ascii
Write-Host "DONE generated loc=$($ruAdd.Count) cursor=$locStart"
