PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAC10",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MAC10_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxMAC10",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "MAC10",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "MAC10",
	group = "Weapons VFX",
	id = "FxMAC10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAC10",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxMAC101",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAC10",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAC102",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAC10",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAC103",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "UZI_reload",
	Source = "ActionPos",
	Target = "MAC10",
	group = "Default",
	id = "fxMAC104",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "MAC10",
	DetailLevel = 100,
	Moment = "start",
	Sound = "UZI_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxMAC105",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "MAC10",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAC106",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "MAC10",
	group = "Default",
	id = "fxMAC107",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "MAC10",
	group = "Default",
	id = "fxMAC108",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAC10",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "UZI_reload",
	group = "Default",
	id = "fxMAC109",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAC10",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxMAC1010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAC10",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxMAC1011",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "MAC10",
	group = "Default",
	id = "fxMAC1012",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "MAC10",
	group = "Default",
	id = "fxMAC1013",
})

