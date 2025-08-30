
--Luger
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Luger",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Luger_shot",
	Target = "Basic",
	group = "Default",
	id = "fxLuger1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Luger",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxLuger2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Luger",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "Luger3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Luger",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "Luger4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Luger",
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
	id = "Luger5",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Luger",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_UpwardFlash",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Luger",
	group = "Weapons VFX",
	id = "Luger5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Luger",
	Time = 200,
	group = "Default",
	id = "Luger6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Luger",
	group = "Default",
	id = "Luger7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Luger",
	Time = 200,
	group = "Default",
	id = "Luger8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Luger",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "Luger9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Luger",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "Luger10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Luger",
	group = "Default",
	id = "Luger11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Luger",
	group = "Default",
	id = "Luger12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Luger",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "Luger13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Luger",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "Luger14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Luger",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "Luger15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Luger",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "Luger16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Luger",
	group = "Default",
	id = "Luger17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "Luger",
	group = "Default",
	id = "Luger18",
})

