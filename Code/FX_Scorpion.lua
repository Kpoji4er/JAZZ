PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Scorpion",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Scorpion_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxScorpion",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Scorpion",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Scorpion",
	group = "Weapons VFX",
	id = "FxScorpion",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Scorpion",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxScorpion1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Scorpion",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxScorpion2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Scorpion",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxScorpion3",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP5_reload",
	Source = "ActionPos",
	Target = "Scorpion",
	group = "Default",
	id = "fxScorpion4",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Scorpion",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP5_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxScorpion5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Scorpion",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxScorpion6",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Scorpion",
	group = "Default",
	id = "fxScorpion7",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "Scorpion",
	group = "Default",
	id = "fxScorpion8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Scorpion",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "MP5_reload",
	group = "Default",
	id = "fxScorpion9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Scorpion",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxScorpion10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Scorpion",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxScorpion11",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Scorpion",
	group = "Default",
	id = "fxScorpion12",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "Scorpion",
	group = "Default",
	id = "fxScorpion13",
})

