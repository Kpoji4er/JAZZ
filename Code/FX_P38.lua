
--P38
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P38",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Luger_shot",
	Target = "Basic",
	group = "Default",
	id = "fxP381",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P38",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxP382",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P38",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "P383",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P38",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "P384",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P38",
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
	id = "P385",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "P38",
	Time = 200,
	group = "Default",
	id = "P386",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "P38",
	group = "Default",
	id = "P387",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "P38",
	Time = 200,
	group = "Default",
	id = "P388",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P38",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bereta92_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "P389",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P38",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "P3810",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P38",
	group = "Default",
	id = "P3811",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P38",
	group = "Default",
	id = "P3812",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P38",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Bereta92_slide-load",
	group = "Default",
	id = "P3813",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P38",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Bereta92_slide-move",
	group = "Default",
	id = "P3814",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P38",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "P3815",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P38",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "P3816",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P38",
	group = "Default",
	id = "P3817",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "P38",
	group = "Default",
	id = "P3818",
})

