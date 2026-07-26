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

function Clamp-Value {
    param(
        [double]$Value,
        [double]$Minimum,
        [double]$Maximum
    )
    return [Math]::Min([Math]::Max($Value, $Minimum), $Maximum)
}

function Round-CTH {
    param([double]$Value)
    return [int][Math]::Round($Value, 0, [MidpointRounding]::AwayFromZero)
}

function Get-AimMastery {
    param([double]$Marksmanship)
    $m = (Clamp-Value $Marksmanship 0 100)
    $value =
        [Math]::Min($m, 60) * 20 / 60 +
        (Clamp-Value ($m - 60) 0 20) * 20 / 20 +
        (Clamp-Value ($m - 80) 0 10) * 20 / 10 +
        (Clamp-Value ($m - 90) 0 6) * 20 / 6 +
        (Clamp-Value ($m - 96) 0 4) * 20 / 4
    return [Math]::Min(100, (Round-CTH $value))
}

function Get-SkillCurve {
    param([double]$Value)
    return 20 + [Math]::Pow([Math]::Max(0, $Value), 1.25) * 0.25
}

function Get-ShooterCore {
    param(
        [hashtable]$Shooter,
        [hashtable]$Weapon,
        [int]$Aim
    )
    $snapRaw = ($Shooter.Dexterity * 4 + $Shooter.Marksmanship + $Shooter.Level * 5) / 6
    $precisionRaw = ($Shooter.Marksmanship * 4 + $Shooter.Dexterity + $Shooter.Level * 5) / 6
    $snap = Get-SkillCurve $snapRaw
    $precision = Get-SkillCurve $precisionRaw
    $aimProgress = if ($Weapon.MaxAimActions -gt 0) {
        (Clamp-Value ($Aim / $Weapon.MaxAimActions) 0 1)
    } else {
        0
    }
    $shotSkill = $snap + $aimProgress * [Math]::Max($precision - $snap, 0)
    $mastery = Get-AimMastery $Shooter.Marksmanship
    $aimGain = [Math]::Max(0, $Aim) * $Weapon.AimAccuracy * $mastery / 100
    return $shotSkill + $aimGain
}

function Get-RangeProfile {
    param(
        [hashtable]$Weapon,
        [double]$Distance,
        [double]$AimProgress,
        [double]$OpticReach = 0,
        [double]$OpticMinRange = 0,
        [double]$OpticNearFactor = 1
    )
    $range = $Weapon.WeaponRange
    if ($Distance -ge $range) {
        return @{
            Possible = $false
            Factor = 0
            EffectiveRange = [Math]::Min($range - 0.01, $Weapon.BulletDropRange + $OpticReach * $AimProgress)
            OpticFactor = 1
        }
    }

    $effective = [Math]::Min($range - 0.01, $Weapon.BulletDropRange + $OpticReach * $AimProgress)
    $power = [Math]::Max(0.25, $Weapon.BulletDropRange * 0.05 + $Weapon.Grouping / 100)
    $factor = if ($Distance -le $effective) {
        1
    } else {
        $t = (Clamp-Value (($Distance - $effective) / ($range - $effective)) 0 1)
        [Math]::Max(1 - [Math]::Pow($t, $power), 0)
    }
    $nearFactor = if ($OpticMinRange -gt 0 -and $Distance -lt $OpticMinRange) {
        $proximity = (Clamp-Value (($OpticMinRange - $Distance) / $OpticMinRange) 0 1)
        1 + ($OpticNearFactor - 1) * $proximity
    } else {
        1
    }

    return @{
        Possible = $true
        Factor = $factor
        EffectiveRange = $effective
        OpticFactor = $nearFactor
    }
}

function Get-FinalChance {
    param(
        [double]$Core,
        [double[]]$Factors,
        [bool]$Possible = $true
    )
    if (!$Possible) {
        return 0
    }
    $product = 1.0
    foreach ($factor in $Factors) {
        $product *= $factor
    }
    return (Clamp-Value (Round-CTH ([Math]::Min($Core, 100) * $product)) 2 100)
}

function Get-RecoilRetention {
    param(
        [double]$Recoil,
        [double]$Strength,
        [double]$StanceFactor = 1,
        [double]$SupportFactor = 1,
        [double]$ComponentFactor = 1,
        [double]$PerkFactor = 1,
        [double]$ActionFactor = 1,
        [double]$ClassFactor = 1
    )
    $strengthFactor = (Clamp-Value (1.25 - $Strength / 200) 0.75 1.25)
    $effective = $Recoil * $strengthFactor * $StanceFactor * $SupportFactor *
        $ComponentFactor * $PerkFactor * $ActionFactor * $ClassFactor
    return (Clamp-Value (1 - $effective / 100) 0.15 1)
}

function Get-BulletChance {
    param(
        [int]$FirstChance,
        [int]$Index,
        [double]$Retention,
        [int]$ProtectedShots = 0
    )
    $exponent = [Math]::Max(0, $Index - 1 - $ProtectedShots)
    return (Clamp-Value (Round-CTH ($FirstChance * [Math]::Pow($Retention, $exponent))) 2 100)
}

function Convert-WeaponRow {
    param($Row)
    return @{
        Id = $Row.id
        MaxAimActions = [int]$Row.max_aim_actions
        AimAccuracy = [int]$Row.aim_accuracy
        Recoil = [int]$Row.recoil
        WeaponRange = [int]$Row.weapon_range
        BulletDropRange = [int]$Row.bullet_drop_range
        Grouping = [int]$Row.grouping
        Handling = [int]$Row.handling
    }
}

$catalogPath = Join-Path $RepoRoot 'docs/technical/weapons/data/weapons.csv'
$catalog = Import-Csv -LiteralPath $catalogPath
$active = @($catalog | Where-Object catalog_status -eq 'active')
$ak = Convert-WeaponRow ($active | Where-Object id -eq 'AK47' | Select-Object -First 1)
$svd = Convert-WeaponRow ($active | Where-Object id -eq 'DragunovSVD' | Select-Object -First 1)

Assert-True ($ak.Id -eq 'AK47') 'AK47 must exist in the canonical active catalog'
Assert-True ($svd.Id -eq 'DragunovSVD') 'DragunovSVD must exist in the canonical active catalog'

$expectedFamilies = @(
    'pistol',
    'autopistol',
    'revolver',
    'submachine-gun',
    'assault-rifle',
    'battle-rifle',
    'sniper-rifle',
    'carbine',
    'shotgun',
    'light-machine-gun',
    'machine-gun'
)
$actualFamilies = @($active.family_id | Sort-Object -Unique)
Assert-True ($actualFamilies.Count -eq 11) 'active catalog must contain exactly eleven weapon families'
foreach ($family in $expectedFamilies) {
    Assert-True ($family -in $actualFamilies) "missing active weapon family: $family"
}
Assert-True (!(($active.object_class + $active.family_id) -match 'CompactSMG')) 'CompactSMG must not be active'
foreach ($excludedId in @('AR15', 'M4Commando', 'MP5')) {
    Assert-True (!(($active | Where-Object id -eq $excludedId))) "$excludedId must not be active"
}

$snapShooter = @{ Dexterity = 95; Marksmanship = 55; Level = 6 }
$precisionShooter = @{ Dexterity = 55; Marksmanship = 95; Level = 6 }
$neutralWeapon = @{
    MaxAimActions = 4
    AimAccuracy = 10
    WeaponRange = 40
    BulletDropRange = 15
    Grouping = 55
    Handling = -100
}

$snapFast = Get-ShooterCore $snapShooter $neutralWeapon 0
$precisionSnap = Get-ShooterCore $precisionShooter $neutralWeapon 0
Assert-True ($snapFast -gt $precisionSnap) 'Dexterity must dominate snap shooting'

$snapAimed = Get-ShooterCore $snapShooter $neutralWeapon 4
$precisionAimed = Get-ShooterCore $precisionShooter $neutralWeapon 4
Assert-True ($precisionAimed -gt $snapAimed) 'Marksmanship must dominate fully aimed shooting'

$previous = -1
foreach ($aim in 0..$neutralWeapon.MaxAimActions) {
    $current = Get-ShooterCore $precisionShooter $neutralWeapon $aim
    Assert-True ($current -ge $previous) "aim click $aim reduced CTH core"
    $previous = $current
}

$handlingVariant = $neutralWeapon.Clone()
$handlingVariant.Handling = 100
Assert-True (
    (Get-ShooterCore $precisionShooter $neutralWeapon 4) -eq
    (Get-ShooterCore $precisionShooter $handlingVariant 4)
) 'Handling must not affect CTH'

$elite = @{ Dexterity = 90; Marksmanship = 100; Level = 10 }
$idealCore = Get-ShooterCore $elite $svd $svd.MaxAimActions
Assert-True ((Get-FinalChance $idealCore @(1.0)) -eq 100) 'ideal full-aim shot must reach 100%'
Assert-True ((Get-FinalChance $idealCore @(0.75)) -eq 75) 'a 0.75 cover factor must lower ideal 100% shot'

$rangeAtEffective = Get-RangeProfile $ak $ak.BulletDropRange 1
$rangeAfterEffective = Get-RangeProfile $ak ($ak.BulletDropRange + 0.001) 1
Assert-True ([Math]::Abs($rangeAtEffective.Factor - 1) -lt 0.000001) 'range factor must be 1 at E'
Assert-True ([Math]::Abs($rangeAfterEffective.Factor - 1) -lt 0.001) 'range curve must be continuous after E'

$nearLimit = Get-RangeProfile $ak ($ak.WeaponRange - 0.001) 1
$nearLimitChance = Get-FinalChance 90 @($nearLimit.Factor) $nearLimit.Possible
Assert-True ($nearLimitChance -eq 2) 'valid shot immediately below physical range must use 2% floor'
$outside = Get-RangeProfile $ak $ak.WeaponRange 1
Assert-True ((Get-FinalChance 100 @(1.0) $outside.Possible) -eq 0) 'shot at physical range must be impossible'

$withOptic = Get-RangeProfile $svd 30 1 12 5 0.75
$withoutOptic = Get-RangeProfile $svd 30 1
Assert-True ($withOptic.EffectiveRange -gt $withoutOptic.EffectiveRange) 'optic must shift effective range'
Assert-True ($withOptic.Possible -eq $withoutOptic.Possible) 'optic must not change physical range'
$nearOptic = Get-RangeProfile $svd 2 1 12 5 0.75
Assert-True ($nearOptic.OpticFactor -lt 1) 'strong optic must have a near-range disadvantage'

$factorOrderA = Get-FinalChance 100 @(0.75, 0.9, 1.1)
$factorOrderB = Get-FinalChance 100 @(1.1, 0.75, 0.9)
Assert-True ($factorOrderA -eq $factorOrderB) 'factor product must not depend on modifier order'

$standingRetention = Get-RecoilRetention 30 50
$supportedRetention = Get-RecoilRetention 30 90 0.75 0.65
Assert-True ($supportedRetention -gt $standingRetention) 'Strength, prone stance and support must improve retention'
$machineGunActionRetention = Get-RecoilRetention 30 50 1 1 1 1 0.8
Assert-True ($machineGunActionRetention -gt $standingRetention) 'MGBurstFire action recoil must improve retention'
$fanningRetention = Get-RecoilRetention 20 50
Assert-True ($fanningRetention -gt $standingRetention) 'Fanning must keep its dedicated recoil profile'
Assert-True ((Get-BulletChance 85 2 $standingRetention 1) -eq 85) 'protected action shot must ignore recoil'
Assert-True ((Get-BulletChance 85 3 $standingRetention 1) -lt 85) 'recoil must resume after protected action shots'
$previousBullet = 101
foreach ($index in 1..12) {
    $bullet = Get-BulletChance 85 $index $standingRetention
    Assert-True ($bullet -le $previousBullet) "bullet $index increased after recoil"
    Assert-True ($bullet -ge 2) "bullet $index fell below the valid-shot floor"
    $previousBullet = $bullet
}

$roleShooter = @{ Dexterity = 75; Marksmanship = 85; Level = 7 }
$comparison = foreach ($distance in @(20, 30, 37)) {
    $akCore = Get-ShooterCore $roleShooter $ak $ak.MaxAimActions
    $svdCore = Get-ShooterCore $roleShooter $svd $svd.MaxAimActions
    $akRange = Get-RangeProfile $ak $distance 1
    $svdRange = Get-RangeProfile $svd $distance 1 12 5 0.75
    $akChance = Get-FinalChance $akCore @($akRange.Factor) $akRange.Possible
    $svdChance = Get-FinalChance $svdCore @($svdRange.Factor, $svdRange.OpticFactor) $svdRange.Possible
    Assert-True ($svdChance -gt $akChance) "SVD must beat AK47 at aimed distance $distance"
    [pscustomobject]@{
        Distance = $distance
        AK47 = $akChance
        SVD = $svdChance
    }
}

$accuracySource = Get-Content -LiteralPath (Join-Path $RepoRoot 'Code/AccuracyRangeCTH.lua') -Raw
$generatedItems = Get-Content -LiteralPath (Join-Path $RepoRoot 'items.lua') -Raw
Assert-True (
    $accuracySource -match 'AbakanBurst = 1' -and
    $accuracySource -match 'JAZZ_ControllableBurst = 1' -and
    $accuracySource -match 'action_id == "MGBurstFire"' -and
    $accuracySource -match 'action_id == "JAZZ_Fanning"'
) 'action-specific recoil contracts must remain in the shared model'
Assert-True ($generatedItems -notmatch '\bBoltingAP\b|\bid = "Bolting"') 'legacy bolting data must be absent'

$comparison | Format-Table -AutoSize
"Shooting model checks passed: active_weapons=$($active.Count), families=$($actualFamilies.Count), assertions=all"
