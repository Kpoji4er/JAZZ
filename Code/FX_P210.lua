
--P210
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P210",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P210_shot",
	Target = "Basic",
	group = "Default",
	id = "fxP2101",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P210",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxP2102",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P210",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "P2103",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P210",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "P2104",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P210",
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
	id = "P2105",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P210",
	Time = 200,
	group = "Default",
	id = "P2106",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P210",
	group = "Default",
	id = "P2107",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P210",
	Time = 200,
	group = "Default",
	id = "P2108",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P210",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "P2109",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P210",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "P21010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P210",
	group = "Default",
	id = "P21011",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P210",
	group = "Default",
	id = "P21012",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P210",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "P21013",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P210",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "P21014",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P210",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "P21015",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P210",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "P21016",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P210",
	group = "Default",
	id = "P21017",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "P210",
	group = "Default",
	id = "P21018",
})

