PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Thompson",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Thompson_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxThompson",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Thompson",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Thompson",
	group = "Weapons VFX",
	id = "FxThompson",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Thompson",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "ParticlesThompson",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Thompson",
	group = "Weapons VFX",
	id = "FxThompson",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Thompson",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxThompson1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Thompson",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxThompson2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Thompson",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxThompson3",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP5_reload",
	Source = "ActionPos",
	Target = "Thompson",
	group = "Default",
	id = "fxThompson4",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Thompson",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP5_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxThompson5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Thompson",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxThompson6",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Thompson",
	group = "Default",
	id = "fxThompson7",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "Thompson",
	group = "Default",
	id = "fxThompson8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Thompson",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "MP5_reload",
	group = "Default",
	id = "fxThompson9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Thompson",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxThompson10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Thompson",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxThompson11",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Thompson",
	group = "Default",
	id = "fxThompson12",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "Thompson",
	group = "Default",
	id = "fxThompson13",
})

