
--DeLisle
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "45welrod_shot",
	Target = "Basic",
	group = "Default",
	id = "fxDeLisle1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxDeLisle2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	Delay = 400,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Gewehr98_reload",
	Source = "ActionPos",
	group = "Default",
	id = "DeLisle3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "DeLisle3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "DeLisle4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "DeLisle",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_Silencer",
	Source = "Target",
	Spot = "Muzzle",
	Target = "DeLisle",
	group = "Weapons VFX",
	id = "DeLisle5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Gewehr98_reload",
	Target = "DeLisle",
	Time = 200,
	group = "Default",
	id = "DeLisle6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_reload",
	Target = "DeLisle",
	group = "Default",
	id = "DeLisle7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "Gewehr98_reload",
	Target = "DeLisle",
	Time = 200,
	group = "Default",
	id = "DeLisle8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "DeLisle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "DeLisle9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "DeLisle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "DeLisle10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "DeLisle",
	group = "Default",
	id = "DeLisle11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "DeLisle",
	group = "Default",
	id = "DeLisle12",
})



PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DeLisle",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "Gewehr98_reload",
	group = "Default",
	id = "DeLisle14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DeLisle",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "DeLisle15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "DeLisle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "DeLisle16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "DeLisle",
	group = "Default",
	id = "DeLisle17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "DeLisle",
	group = "Default",
	id = "DeLisle18",
})

