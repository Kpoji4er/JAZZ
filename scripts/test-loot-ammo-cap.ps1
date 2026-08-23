param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )
    if (!$Condition) {
        throw "ASSERTION FAILED: $Message"
    }
}

function Get-MulDivRound {
    param(
        [int]$A,
        [int]$B,
        [int]$C
    )
    if ($C -eq 0) {
        throw 'MulDivRound divisor is 0'
    }
    return [int][Math]::Floor(($A * $B + [Math]::Floor($C / 2)) / $C)
}

$Keep = @{
    Normal   = @{ other = 80; mg = 50 }
    Hard     = @{ other = 60; mg = 30 }
    VeryHard = @{ other = 45; mg = 18 }
}

function Get-LootAmmoKeepPercent {
    param(
        [string]$Difficulty,
        [bool]$IsMG
    )
    $row = $Keep[$Difficulty]
    if ($null -eq $row) {
        $row = $Keep.Normal
    }
    if ($IsMG) {
        return [int]$row.mg
    }
    return [int]$row.other
}

function Get-LootFirearmAmmoCap {
    param(
        [int]$MagazineSize,
        [int]$Amount,
        [string]$Difficulty,
        [bool]$IsMG
    )
    if ($Amount -le 0) {
        return 0
    }
    $pct = Get-LootAmmoKeepPercent -Difficulty $Difficulty -IsMG $IsMG
    $cap = [Math]::Max(1, (Get-MulDivRound -A $MagazineSize -B $pct -C 100))
    if ($Amount -gt $cap) {
        return $cap
    }
    return $Amount
}

$lootDrops = Get-Content -LiteralPath (Join-Path $RepoRoot 'Code\System_LootDrops.lua') -Raw
Assert-True ($lootDrops -match 'JAZZ_LOOT_AMMO_KEEP') 'needle: JAZZ_LOOT_AMMO_KEEP table'
Assert-True ($lootDrops -match 'Normal\s*=\s*\{\s*other\s*=\s*80,\s*mg\s*=\s*50\s*\}') 'needle: Normal 80/50'
Assert-True ($lootDrops -match 'Hard\s*=\s*\{\s*other\s*=\s*60,\s*mg\s*=\s*30\s*\}') 'needle: Hard 60/30'
Assert-True ($lootDrops -match 'VeryHard\s*=\s*\{\s*other\s*=\s*45,\s*mg\s*=\s*18\s*\}') 'needle: VeryHard 45/18'
Assert-True ($lootDrops -match 'if is_npc and IsKindOf\(item, "Firearm"\)') 'needle: cap only NPC firearms'
Assert-True ($lootDrops -match 'JAZZ_CapLootFirearmAmmo\(item, Game and Game\.game_difficulty\)') 'needle: difficulty from Game.game_difficulty'
Assert-True ($lootDrops -match 'IsKindOf\(item, "MachineGun"\) or IsKindOf\(item, "LightMachineGun"\)') 'needle: sibling MG classes'

$orUnit = Get-Content -LiteralPath (Join-Path $RepoRoot 'Code\System_OR_Unit.lua') -Raw
Assert-True ($orUnit -match 'tempAmmo\.Amount = weapon\.MagazineSize') 'EquipStartingGear still fills a full mag'
Assert-True ($orUnit -notmatch 'JAZZ_CapLootFirearmAmmo') 'EquipStartingGear is not the loot cap hook'

$aiActions = Get-Content -LiteralPath (Join-Path $RepoRoot 'Code\AiActions.lua') -Raw
Assert-True ($aiActions -match 'ammo\.Amount = firearm\.MagazineSize') 'AI refill still uses MagazineSize'
Assert-True ($aiActions -notmatch 'JAZZ_CapLootFirearmAmmo') 'AiActions is not the loot cap hook'

Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'Normal' -IsMG:$false) -eq 80) 'other Normal 80'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'Hard' -IsMG:$false) -eq 60) 'other Hard 60'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'VeryHard' -IsMG:$false) -eq 45) 'other VeryHard 45'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'Normal' -IsMG:$true) -eq 50) 'mg Normal 50'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'Hard' -IsMG:$true) -eq 30) 'mg Hard 30'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'VeryHard' -IsMG:$true) -eq 18) 'mg VeryHard 18'
Assert-True ((Get-LootAmmoKeepPercent -Difficulty 'Easy' -IsMG:$true) -eq 50) 'unknown difficulty uses Normal'

Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 100 -Amount 100 -Difficulty 'Normal' -IsMG:$true) -eq 50) 'PKM Normal 50'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 100 -Amount 100 -Difficulty 'Hard' -IsMG:$true) -eq 30) 'PKM Hard 30'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 100 -Amount 100 -Difficulty 'VeryHard' -IsMG:$true) -eq 18) 'PKM VeryHard 18'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 100 -Amount 12 -Difficulty 'VeryHard' -IsMG:$true) -eq 12) 'remainder below cap stays'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 100 -Amount 0 -Difficulty 'Normal' -IsMG:$true) -eq 0) 'empty mag stays empty'

Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 30 -Amount 30 -Difficulty 'Normal' -IsMG:$false) -eq 24) 'AK Normal 24'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 30 -Amount 30 -Difficulty 'Hard' -IsMG:$false) -eq 18) 'AK Hard 18'
Assert-True ((Get-LootFirearmAmmoCap -MagazineSize 30 -Amount 30 -Difficulty 'VeryHard' -IsMG:$false) -eq 14) 'AK VeryHard 14'

Write-Host 'loot ammo cap tests: PASS'
