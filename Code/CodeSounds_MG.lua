
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BrowningM2HMG",
	DetailLevel = 100,
	Moment = "start",
	Sound = "BrowningM2HMG_shot_single",
	Target = "any",
	group = "Default",
	id = "fxBrowningM2HMG",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MG42",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_shot_single",
	Target = "any",
	group = "Default",
	id = "fxMG42",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MG58",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_shot_single",
	Target = "any",
	group = "Default",
	id = "fxMG58",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "MAC2429",
	Inherit = "MG42",
	group = "Weapons VFX",
	id = "fxMAC2429",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "MAC2429",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAC2429",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bren_shot",
	Target = "any",
	group = "Default",
	id = "fxMAC2429",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M60",
	Inherit = "FNMinimi",
	group = "Weapons VFX",
	id = "fxM60",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "M60",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M60",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M60_shot",
	Target = "any",
	group = "Default",
	id = "fxM60",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M60E3",
	Inherit = "M60",
	group = "Weapons VFX",
	id = "fxM60E3",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M60E4",
	Inherit = "M60",
	group = "Weapons VFX",
	id = "fxM60E4",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "U100",
	Inherit = "FNMinimi",
	group = "Weapons VFX",
	id = "fxU100",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "FNMAG",
	Inherit = "FNMinimi",
	group = "Weapons VFX",
	id = "fxFNMAG",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "FNMAG",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "FNMAG",
	DetailLevel = 100,
	Moment = "start",
	Sound = "FNMAG_shot",
	Target = "any",
	group = "Default",
	id = "fxFNMAG",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "PKM",
	Inherit = "FNMinimi",
	group = "Weapons VFX",
	id = "fxPKM",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "PKM",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PKM",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PKM_shot",
	Target = "any",
	group = "Default",
	id = "fxPKM",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "HK23e",
	Inherit = "HK21",
	group = "Weapons VFX",
	id = "fxHK23e",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "HK23e",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "HK23e",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HK23e_shot",
	Target = "any",
	group = "Default",
	id = "fxHK23e",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_shot",
	Target = "any",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_equipncheck",
	Target = "MachineGun",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxDP27",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "DP27",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "MachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "dp27",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "MachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "DP27",
	group = "Default",
	id = "fxDP27",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "MachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "dp27_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "DP27",
	group = "Default",
	id = "fxDP27",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "MachineGun",
	DetailLevel = 100,
	Delay = 500,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "DP27",
	group = "Default",
	id = "fxDP27",
})
