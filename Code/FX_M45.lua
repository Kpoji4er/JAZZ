PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M45_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxM45",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "M45",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "M45",
	group = "Weapons VFX",
	id = "FxM45",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxM451",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M45",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxM452",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M45",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxM453",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "RPK74_reload",
	Source = "ActionPos",
	Target = "M45",
	group = "Default",
	id = "fxM454",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "M45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "RPK74_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxM455",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "M45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxM456",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "M45",
	group = "Default",
	id = "fxM457",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "M45",
	group = "Default",
	id = "fxM458",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M45",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "RPK74_reload",
	group = "Default",
	id = "fxM459",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M45",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxM4510",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M45",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxM4511",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "M45",
	group = "Default",
	id = "fxM4512",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "M45",
	group = "Default",
	id = "fxM4513",
})

