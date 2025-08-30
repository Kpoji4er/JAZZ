
--SWModel52
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "38sw_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSWModel521",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxSWModel522",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel52",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "SWModel523",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel52",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "SWModel524",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "SWModel52",
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
	id = "SWModel525",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel52",
	Time = 200,
	group = "Default",
	id = "SWModel526",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel52",
	group = "Default",
	id = "SWModel527",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel52",
	Time = 200,
	group = "Default",
	id = "SWModel528",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "SWModel52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "SWModel529",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "SWModel52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "SWModel5210",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "SWModel52",
	group = "Default",
	id = "SWModel5211",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "SWModel52",
	group = "Default",
	id = "SWModel5212",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel52",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "SWModel5213",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel52",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "SWModel5214",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel52",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "SWModel5215",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "SWModel5216",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "SWModel52",
	group = "Default",
	id = "SWModel5217",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "SWModel52",
	group = "Default",
	id = "SWModel5218",
})

