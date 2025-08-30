
--Colt1911
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Colt1911",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Colt1911_shot",
	Target = "Basic",
	group = "Default",
	id = "fxColt19111",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Colt1911",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxColt19112",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Colt1911",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "Colt19113",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Colt1911",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "Colt19114",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Colt1911",
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
	id = "Colt19115",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Colt1911",
	Time = 200,
	group = "Default",
	id = "Colt19116",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Colt1911",
	group = "Default",
	id = "Colt19117",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "Colt1911",
	Time = 200,
	group = "Default",
	id = "Colt19118",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Colt1911",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "Colt19119",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Colt1911",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "Colt191110",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Colt1911",
	group = "Default",
	id = "Colt191111",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Colt1911",
	group = "Default",
	id = "Colt191112",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Colt1911",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "Colt191113",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Colt1911",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "Colt191114",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Colt1911",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "Colt191115",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Colt1911",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "Colt191116",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Colt1911",
	group = "Default",
	id = "Colt191117",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "Colt1911",
	group = "Default",
	id = "Colt191118",
})

