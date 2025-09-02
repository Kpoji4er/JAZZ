
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "G3",
	DetailLevel = 100,
	Moment = "start",
	Sound = "G3_shot",
	Target = "Basic",
	group = "Default",
	id = "fxG3",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HK21_reload",
	Target = "G3",
	group = "Default",
	id = "fxG32",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "G3",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HK21_reload",
	Source = "Camera",
	Target = "AssaultRifle",
	group = "Default",
	id = "fxG33",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "G3",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxG34",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "G3",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxG35",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "G3",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingB_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxG36",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "G3",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_shotgun",
	group = "Default",
	id = "fxG37",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-762",
	Source = "Camera",
	Target = "G3",
	group = "Default",
	id = "fxG38",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 900,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-load",
	Source = "Camera",
	Target = "G3",
	group = "Default",
	id = "fxG39",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "G3",
	Delay = 1500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HK21_reload",
	group = "Default",
	id = "fxG310",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "G3",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_rifle-load",
	group = "Default",
	id = "fxG311",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 900,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-762",
	Source = "Camera",
	Target = "G3",
	group = "Default",
	id = "fxG312",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-unload",
	Source = "Camera",
	Target = "G3",
	group = "Default",
	id = "fxG313",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "G3SniperV1",
	Inherit = "G3A3",
	group = "Weapons VFX",
	id = "fxG3",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "G3A4",
	Inherit = "G3A3",
	group = "Weapons VFX",
	id = "fxG3",
})