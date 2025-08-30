
--FiveSeven
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "FiveSeven",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90_shot",
	Target = "Basic",
	group = "Default",
	id = "fxFiveSeven1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "FiveSeven",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxFiveSeven2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "FiveSeven",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "FiveSeven3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "FiveSeven",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "FiveSeven4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "FiveSeven",
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
	id = "FiveSeven5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "FiveSeven",
	Time = 200,
	group = "Default",
	id = "FiveSeven6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "FiveSeven",
	group = "Default",
	id = "FiveSeven7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Bereta92_reload",
	Target = "FiveSeven",
	Time = 200,
	group = "Default",
	id = "FiveSeven8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "FiveSeven",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bereta92_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "FiveSeven9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "FiveSeven",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "FiveSeven10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "FiveSeven",
	group = "Default",
	id = "FiveSeven11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "FiveSeven",
	group = "Default",
	id = "FiveSeven12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "FiveSeven",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Bereta92_slide-load",
	group = "Default",
	id = "FiveSeven13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "FiveSeven",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Bereta92_slide-move",
	group = "Default",
	id = "FiveSeven14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "FiveSeven",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "FiveSeven15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "FiveSeven",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "FiveSeven16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "FiveSeven",
	group = "Default",
	id = "FiveSeven17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "FiveSeven",
	group = "Default",
	id = "FiveSeven18",
})

