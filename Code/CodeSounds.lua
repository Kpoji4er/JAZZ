
-- WeaponFire/WeaponAutoFire resolve fx_target from visual_obj.parts.Muzzle or .Barrel
-- (Weapon.lua). Vanilla ActionFX for AKSU/AK74/etc. use Target = "Basic" / "Silencer".
-- Vanilla Compensator/MuzzleBooster/BarrelNormal inherit Basic; JAZZ_* twins must too,
-- otherwise default JAZZ_Compensator (AKSU etc.) → silent shots.

local function JazzFxInherit(actor, inherit, id)
	PlaceObj('ActionFXInherit_Actor', {
		Actor = actor,
		Inherit = inherit,
		group = "Weapons VFX",
		id = id,
	})
end

-- Loud muzzle / barrel FX targets → Basic (shot sound + muzzle flash particles)
JazzFxInherit("JAZZ_Compensator", "Basic", "fxJAZZ_Compensator")
JazzFxInherit("JAZZ_FlashHider", "Basic", "fxJAZZ_FlashHider")
JazzFxInherit("JAZZ_DefMuzzle", "Basic", "fxJAZZ_DefMuzzle")
JazzFxInherit("JAZZ_M14_Default_Muzzle", "Basic", "fxJAZZ_M14_Default_Muzzle")
JazzFxInherit("JAZZ_Galil_Brake_Default", "Basic", "fxJAZZ_Galil_Brake_Default")
JazzFxInherit("JAZZ_DuckbillChoke", "Basic", "fxJAZZ_DuckbillChoke")
JazzFxInherit("JAZZ_FullChoke", "Basic", "fxJAZZ_FullChoke")
JazzFxInherit("JAZZ_BarrelNormal", "Basic", "fxJAZZ_BarrelNormal")
JazzFxInherit("JAZZ_BarrelNormalImproved", "Basic", "fxJAZZ_BarrelNormalImproved")
JazzFxInherit("JAZZ_BarrelNormal_Sil", "Basic", "fxJAZZ_BarrelNormal_Sil")
JazzFxInherit("JAZZ_BarrelNormal_noSil", "Basic", "fxJAZZ_BarrelNormal_noSil")
JazzFxInherit("JAZZ_BarrelShort", "Basic", "fxJAZZ_BarrelShort")
JazzFxInherit("JAZZ_BarrelShortImproved", "Basic", "fxJAZZ_BarrelShortImproved")
JazzFxInherit("JAZZ_BarrelShort_Pistol", "Basic", "fxJAZZ_BarrelShort_Pistol")
JazzFxInherit("JAZZ_BarrelShortRunNGun", "Basic", "fxJAZZ_BarrelShortRunNGun")
JazzFxInherit("JAZZ_BarrelShortShotgun", "Basic", "fxJAZZ_BarrelShortShotgun")
JazzFxInherit("JAZZ_BarrelShortShotgun_Benelli", "Basic", "fxJAZZ_BarrelShortShotgun_Benelli")
JazzFxInherit("JAZZ_BarrelShort_AUG", "Basic", "fxJAZZ_BarrelShort_AUG")
JazzFxInherit("JAZZ_BarrelShortImproved_AUG", "Basic", "fxJAZZ_BarrelShortImproved_AUG")
JazzFxInherit("JAZZ_BarrelLong", "Basic", "fxJAZZ_BarrelLong")
JazzFxInherit("JAZZ_BarrelLongImproved", "Basic", "fxJAZZ_BarrelLongImproved")
JazzFxInherit("JAZZ_BarrelLongShotgun", "Basic", "fxJAZZ_BarrelLongShotgun")
JazzFxInherit("JAZZ_BarrelLong_AUG", "Basic", "fxJAZZ_BarrelLong_AUG")
JazzFxInherit("JAZZ_BarrelLongImproved_AUG", "Basic", "fxJAZZ_BarrelLongImproved_AUG")
JazzFxInherit("JAZZ_BarrelHeavy", "Basic", "fxJAZZ_BarrelHeavy")
JazzFxInherit("JAZZ_Barrel50BMG_DesertEagle", "Basic", "fxJAZZ_Barrel50BMG_DesertEagle")
-- Auto5 barrel/mag configs (vanilla Auto5_* → Basic; JAZZ twin IDs need the same)
JazzFxInherit("JAZZ_Auto5_Basic_LMag", "Basic", "fxJAZZ_Auto5_Basic_LMag")
JazzFxInherit("JAZZ_Auto5_Basic_NMag", "Basic", "fxJAZZ_Auto5_Basic_NMag")
JazzFxInherit("JAZZ_Auto5_Long_LMag", "Basic", "fxJAZZ_Auto5_Long_LMag")
JazzFxInherit("JAZZ_Auto5_Long_NMag", "Basic", "fxJAZZ_Auto5_Long_NMag")
JazzFxInherit("JAZZ_Auto5_Short_NMag", "Basic", "fxJAZZ_Auto5_Short_NMag")
-- Removable bag twins that may still be equipped after AUG/HK21 slot remount to vanilla IDs
JazzFxInherit("JAZZ_AUGCompensator_01", "Basic", "fxJAZZ_AUGCompensator_01")
JazzFxInherit("JAZZ_AUGCompensator_03", "Basic", "fxJAZZ_AUGCompensator_03")

-- Suppressors → Silencer (quiet shot bank)
JazzFxInherit("JAZZ_Suppressor", "Silencer", "fxJAZZ_Suppressor")
JazzFxInherit("JAZZ_SuppressorImproved", "Silencer", "fxJAZZ_SuppressorImproved")
JazzFxInherit("JAZZ_SuppressorIntegrated", "Silencer", "fxJAZZ_SuppressorIntegrated")
JazzFxInherit("JAZZ_ImprovisedSuppressor", "Silencer", "fxJAZZ_ImprovisedSuppressor")

-- Legacy unprefixed aliases (older CodeSounds / leftover component ids)
JazzFxInherit("SuppressorIntegrated", "Silencer", "fxSuppressorIntegrated")
JazzFxInherit("PistolSuppressor", "Silencer", "fxPistolSuppressor")
JazzFxInherit("SuppressorImproved", "Silencer", "fxSuppressorImproved")
JazzFxInherit("BarrelShortRunNGun", "Basic", "fxBarrelShortRunNGun")
JazzFxInherit("BarrelShort_Pistol", "Basic", "fxBarrelShort_Pistol")
JazzFxInherit("BarrelNormal_Sil", "Basic", "fxBarrelNormal_Sil")
JazzFxInherit("BarrelNormal_noSil", "Basic", "fxBarrelNormal_noSil")
JazzFxInherit("DefMuzzle", "Basic", "fxDefMuzzle")
JazzFxInherit("FlashHider", "Basic", "fxFlashHider")



-- M24Sniper fire FX lives in Code/FX_M24Sniper.lua

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M79",
	Inherit = "UnderslungGrenadeLauncher",
	group = "Weapons VFX",
	id = "fxM79",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponReload",
	Actor = "M79",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M79",
	DetailLevel = 100,
	Moment = "start",
	Sound = "m79_clipout",
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM79",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M79",
	DetailLevel = 100,
	Moment = "start",
	Sound = "m79_clipin",
	Delay = 2200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM79",
})

-- No m79_reload preset/samples; finish reload with equipncheck as closest remaining handling cue
PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M79",
	DetailLevel = 100,
	Moment = "start",
	Sound = "m79_equipncheck",
	Delay = 4200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM79",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponEquip",
	Actor = "M79",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "M79",
	DetailLevel = 100,
	Moment = "start",
	Sound = "m79_equipncheck",
	Target = "GrenadeLauncher",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxM79",
})

-- China_Lake inherits M79 → UnderslungGrenadeLauncher fire; do not override with equipncheck
PlaceObj('ActionFXInherit_Actor', {
	Actor = "China_Lake",
	Inherit = "M79",
	group = "Weapons VFX",
	id = "fxChina_Lake",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "JAZZ_AMMO_MortarShell_HE",
	Inherit = "MortarShell_HE",
	group = "Weapons VFX",
	id = "fxJAZZ_MortarShell_HE",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "JAZZ_AMMO_MortarShell_Gas",
	Inherit = "MortarShell_Gas",
	group = "Weapons VFX",
	id = "fxJAZZ_MortarShell_Gas",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "JAZZ_AMMO_MortarShell_Smoke",
	Inherit = "MortarShell_Smoke",
	group = "Weapons VFX",
	id = "fxJAZZ_MortarShell_Smoke",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "JAZZ_AMMO_40mmFragGrenade",
	Inherit = "_40mmFragGrenade",
	group = "Weapons VFX",
	id = "fxJAZZ_40mmFragGrenade",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "JAZZ_AMMO_40mmFlashbangGrenade",
	Inherit = "_40mmFlashbangGrenade",
	group = "Weapons VFX",
	id = "fxJAZZ_40mmFlashbangGrenade",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "Galil_FlagHill",
	Inherit = "Galil",
	group = "Weapons VFX",
	id = "fxGalil_FlagHill",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "GoldenGun",
	Inherit = "M14SAW",
	group = "Weapons VFX",
	id = "fxGoldenGun",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "LionRoar",
	Inherit = "UZI",
	group = "Weapons VFX",
	id = "fxLionRoar",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "Winchester_Quest",
	Inherit = "Winchester1894",
	group = "Weapons VFX",
	id = "fxWinchester_Quest",
})

