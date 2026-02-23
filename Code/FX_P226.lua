PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P226_temp",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "P226_temp",
	group = "Weapons VFX",
	id = "FxP226_temp",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226_temp",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P226_temp_shot",
	Target = "Basic",
	group = "Default",
	id = "fxP226_temp1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226_temp",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxP226_temp2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226_temp",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "P226_temp3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226_temp",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "P226_temp4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P226_temp",
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
	id = "P226_temp5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226_temp",
	Time = 200,
	group = "Default",
	id = "P226_temp6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226_temp",
	group = "Default",
	id = "P226_temp7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226_temp",
	Time = 200,
	group = "Default",
	id = "P226_temp8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P226_temp",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "P226_temp9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P226_temp",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "P226_temp10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P226_temp",
	group = "Default",
	id = "P226_temp11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P226_temp",
	group = "Default",
	id = "P226_temp12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226_temp",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "P226_temp13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226_temp",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "P226_temp14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226_temp",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "P226_temp15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226_temp",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "P226_temp16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P226_temp",
	group = "Default",
	id = "P226_temp17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "P226_temp",
	group = "Default",
	id = "P226_temp18",
})