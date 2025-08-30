PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P220",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "P220",
	group = "Weapons VFX",
	id = "FxP220",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P220",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P220_shot",
	Target = "Basic",
	group = "Default",
	id = "fxP2201",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P220",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxP2202",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P220",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "P2203",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P220",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "P2204",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P220",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_UpwardFlash",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Compensator",
	group = "Weapons VFX",
	id = "P2205",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P220",
	Time = 200,
	group = "Default",
	id = "P2206",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P220",
	group = "Default",
	id = "P2207",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P220",
	Time = 200,
	group = "Default",
	id = "P2208",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P220",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "P2209",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P220",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "P22010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P220",
	group = "Default",
	id = "P22011",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P220",
	group = "Default",
	id = "P22012",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P220",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "P22013",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P220",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "P22014",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P220",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "P22015",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P220",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "P22016",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P220",
	group = "Default",
	id = "P22017",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "P220",
	group = "Default",
	id = "P22018",
})