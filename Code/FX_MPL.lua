PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MPL",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MPL_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxMPL",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "MPL",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "MPL",
	group = "Weapons VFX",
	id = "FxMPL",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MPL",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxMPL1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MPL",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxMPL2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MPL",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxMPL3",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP40_reload",
	Source = "ActionPos",
	Target = "MPL",
	group = "Default",
	id = "fxMPL4",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "MPL",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP40_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxMPL5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "MPL",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxMPL6",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "MPL",
	group = "Default",
	id = "fxMPL7",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "MPL",
	group = "Default",
	id = "fxMPL8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MPL",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "MP40_reload",
	group = "Default",
	id = "fxMPL9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MPL",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxMPL10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MPL",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxMPL11",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "MPL",
	group = "Default",
	id = "fxMPL12",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "MPL",
	group = "Default",
	id = "fxMPL13",
})

