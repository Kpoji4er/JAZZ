

PlaceObj('ActionFXInherit_Actor', {
	Actor = "SuppressorIntegrated",
	Inherit = "Silencer",
	group = "Weapons VFX",
	id = "fxSuppressorIntegrated",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "PistolSuppressor",
	Inherit = "Silencer",
	group = "Weapons VFX",
	id = "fxPistolSuppressor",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "SuppressorImproved",
	Inherit = "Silencer",
	group = "Weapons VFX",
	id = "fxSuppressorImproved",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "BarrelShortRunNGun",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxBarrelShortRunNGun",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "BarrelShort_Pistol",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxBarrelShort_Pistol",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "BarrelNormal_Sil",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxBarrelNormal_Sil",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "BarrelNormal_noSil",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxBarrelNormal_noSil",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "DefMuzzle",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxDefMuzzle",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "flashhider",
	Inherit = "Basic",
	group = "Weapons VFX",
	id = "fxflashhider",
})



--PlaceObj('ActionFXSound', {
--	Action = "WeaponFire",
--	Actor = "M24Sniper",
--	DetailLevel = 100,
--	Moment = "start",
--	Sound = "M24Sniper_shot",
--	Target = "any",
--	group = "Default",
--	id = "fxM24Sniper",
--})





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

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M79",
	DetailLevel = 100,
	Moment = "start",
	Sound = "m79_reload",
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





PlaceObj('ActionFXInherit_Actor', {
	Actor = "China_Lake",
	Inherit = "M79",
	group = "Weapons VFX",
	id = "fxChina_Lake",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "China_Lake",
	DetailLevel = 100,
	Moment = "start",
	Sound = "gm94_equipncheck",
	Delay = 500,
	Target = "any",
	group = "Default",
	id = "fxChina_Lake",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "China_Lake",
	DetailLevel = 100,
	Moment = "start",
	Sound = "gm94_equipncheck",
	Delay = 500,
	Target = "Basic",
	group = "Default",
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

