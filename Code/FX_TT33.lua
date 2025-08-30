
--TT33
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TT33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "TT33_shot",
	Target = "Basic",
	group = "Default",
	id = "fxTT331",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TT33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxTT332",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TT33",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "TT333",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TT33",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "TT334",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "TT33",
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
	id = "TT335",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "TT33",
	Time = 200,
	group = "Default",
	id = "TT336",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "TT33",
	group = "Default",
	id = "TT337",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "TT33",
	Time = 200,
	group = "Default",
	id = "TT338",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "TT33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "TT339",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "TT33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "TT3310",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "TT33",
	group = "Default",
	id = "TT3311",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "TT33",
	group = "Default",
	id = "TT3312",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TT33",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "TT3313",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TT33",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "TT3314",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TT33",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "TT3315",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TT33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "TT3316",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "TT33",
	group = "Default",
	id = "TT3317",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "TT33",
	group = "Default",
	id = "TT3318",
})

