PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "UMP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "UMP45_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxUMP45",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "UMP45",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "UMP45",
	group = "Weapons VFX",
	id = "FxUMP45",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "UMP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxUMP451",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "UMP45",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxUMP452",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "UMP45",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxUMP453",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_reload",
	Source = "ActionPos",
	Target = "UMP45",
	group = "Default",
	id = "fxUMP454",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "UMP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxUMP455",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "UMP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxUMP456",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "UMP45",
	group = "Default",
	id = "fxUMP457",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "UMP45",
	group = "Default",
	id = "fxUMP458",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "UMP45",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "MG42_reload",
	group = "Default",
	id = "fxUMP459",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "UMP45",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxUMP4510",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "UMP45",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxUMP4511",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "UMP45",
	group = "Default",
	id = "fxUMP4512",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "UMP45",
	group = "Default",
	id = "fxUMP4513",
})

