
--Welrod
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Welrod",
	DetailLevel = 100,
	Moment = "start",
	Sound = "45welrod_shot",
	Target = "Basic",
	group = "Default",
	id = "fxWelrod1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Welrod",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxWelrod2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Welrod",
	Delay = 400,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "45welrod_reload",
	Source = "ActionPos",
	group = "Default",
	id = "Welrod3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Welrod",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "Welrod3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Welrod",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "Welrod4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Welrod",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_Silencer",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Welrod",
	group = "Weapons VFX",
	id = "Welrod5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "45welrod_reload",
	Target = "Welrod",
	Time = 200,
	group = "Default",
	id = "Welrod6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "45welrod_reload",
	Target = "Welrod",
	group = "Default",
	id = "Welrod7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "45welrod_reload",
	Target = "Welrod",
	Time = 200,
	group = "Default",
	id = "Welrod8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Welrod",
	DetailLevel = 100,
	Moment = "start",
	Sound = "45welrod_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "Welrod9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Welrod",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "Welrod10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Welrod",
	group = "Default",
	id = "Welrod11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Welrod",
	group = "Default",
	id = "Welrod12",
})



PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Welrod",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "45welrod_reload",
	group = "Default",
	id = "Welrod14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Welrod",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "Welrod15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Welrod",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "Welrod16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Welrod",
	group = "Default",
	id = "Welrod17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "Welrod",
	group = "Default",
	id = "Welrod18",
})

