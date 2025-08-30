
--USP45
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "USP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "USP45_shot",
	Target = "Basic",
	group = "Default",
	id = "fxUSP451",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "USP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxUSP452",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "USP45",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "USP453",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "USP45",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "USP454",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "USP45",
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
	id = "USP455",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "USP45",
	Time = 200,
	group = "Default",
	id = "USP456",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "USP45",
	group = "Default",
	id = "USP457",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "USP45",
	Time = 200,
	group = "Default",
	id = "USP458",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "USP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "USP459",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "USP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "USP4510",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "USP45",
	group = "Default",
	id = "USP4511",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "USP45",
	group = "Default",
	id = "USP4512",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "USP45",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "USP4513",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "USP45",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "USP4514",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "USP45",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "USP4515",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "USP45",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "USP4516",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "USP45",
	group = "Default",
	id = "USP4517",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "USP45",
	group = "Default",
	id = "USP4518",
})

