
--VectorCP1
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "VectorCP1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "38sw_shot",
	Target = "Basic",
	group = "Default",
	id = "fxVectorCP11",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "VectorCP1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxVectorCP12",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "VectorCP1",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "VectorCP13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "VectorCP1",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "VectorCP14",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "VectorCP1",
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
	id = "VectorCP15",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "VectorCP1",
	Time = 200,
	group = "Default",
	id = "VectorCP16",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "VectorCP1",
	group = "Default",
	id = "VectorCP17",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "VectorCP1",
	Time = 200,
	group = "Default",
	id = "VectorCP18",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "VectorCP1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "VectorCP19",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "VectorCP1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "VectorCP110",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "VectorCP1",
	group = "Default",
	id = "VectorCP111",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "VectorCP1",
	group = "Default",
	id = "VectorCP112",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VectorCP1",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "VectorCP113",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VectorCP1",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "VectorCP114",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VectorCP1",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "VectorCP115",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VectorCP1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "VectorCP116",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "VectorCP1",
	group = "Default",
	id = "VectorCP117",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "VectorCP1",
	group = "Default",
	id = "VectorCP118",
})

