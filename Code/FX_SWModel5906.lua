
--SWModel5906
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel5906",
	DetailLevel = 100,
	Moment = "start",
	Sound = "38sw_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSWModel59061",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel5906",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxSWModel59062",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel5906",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "SWModel59063",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SWModel5906",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "SWModel59064",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "SWModel5906",
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
	id = "SWModel59065",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel5906",
	Time = 200,
	group = "Default",
	id = "SWModel59066",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel5906",
	group = "Default",
	id = "SWModel59067",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "SWModel5906",
	Time = 200,
	group = "Default",
	id = "SWModel59068",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "SWModel5906",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "SWModel59069",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "SWModel5906",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "SWModel590610",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "SWModel5906",
	group = "Default",
	id = "SWModel590611",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "SWModel5906",
	group = "Default",
	id = "SWModel590612",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel5906",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "SWModel590613",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel5906",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "SWModel590614",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel5906",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "SWModel590615",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SWModel5906",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "SWModel590616",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "SWModel5906",
	group = "Default",
	id = "SWModel590617",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "SWModel5906",
	group = "Default",
	id = "SWModel590618",
})

