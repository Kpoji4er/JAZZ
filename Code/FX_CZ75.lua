
--CZ75
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ75",
	DetailLevel = 100,
	Moment = "start",
	Sound = "CZ75_shot",
	Target = "Basic",
	group = "Default",
	id = "fxCZ751",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ75",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxCZ752",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ75",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "CZ753",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ75",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "CZ754",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "CZ75",
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
	id = "CZ755",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "CZ75",
	Time = 200,
	group = "Default",
	id = "CZ756",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "CZ75",
	group = "Default",
	id = "CZ757",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "CZ75",
	Time = 200,
	group = "Default",
	id = "CZ758",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "CZ75",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "CZ759",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "CZ75",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "CZ7510",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "CZ75",
	group = "Default",
	id = "CZ7511",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "CZ75",
	group = "Default",
	id = "CZ7512",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ75",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "CZ7513",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ75",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "CZ7514",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ75",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "CZ7515",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ75",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "CZ7516",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "CZ75",
	group = "Default",
	id = "CZ7517",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "CZ75",
	group = "Default",
	id = "CZ7518",
})

