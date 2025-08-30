PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BerettaM12",
	DetailLevel = 100,
	Moment = "start",
	Sound = "BerettaM12_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxBerettaM12",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "BerettaM12",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "BerettaM12",
	group = "Weapons VFX",
	id = "FxBerettaM12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BerettaM12",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxBerettaM121",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BerettaM12",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxBerettaM122",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BerettaM12",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxBerettaM123",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "G36_reload",
	Source = "ActionPos",
	Target = "BerettaM12",
	group = "Default",
	id = "fxBerettaM124",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "BerettaM12",
	DetailLevel = 100,
	Moment = "start",
	Sound = "G36_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxBerettaM125",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "BerettaM12",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxBerettaM126",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "BerettaM12",
	group = "Default",
	id = "fxBerettaM127",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "BerettaM12",
	group = "Default",
	id = "fxBerettaM128",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "BerettaM12",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "G36_reload",
	group = "Default",
	id = "fxBerettaM129",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "BerettaM12",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxBerettaM1210",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "BerettaM12",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxBerettaM1211",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "BerettaM12",
	group = "Default",
	id = "fxBerettaM1212",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "BerettaM12",
	group = "Default",
	id = "fxBerettaM1213",
})

