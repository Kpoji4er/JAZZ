PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "APS_shot",
	Target = "Basic",
	group = "Default",
	id = "fxAPS1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxAPS2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "APS",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "APS3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "APS",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "APS4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "APS",
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
	id = "APS5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxAPS_unjam1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxAPS_unjam2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxAPS_unjam3",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_equipncheck",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "APS9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "APS10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "APS",
	group = "Default",
	id = "APS11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "APS",
	group = "Default",
	id = "APS12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxAPS13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxAPS14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "APS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxAPS15",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "APS",
	group = "Default",
	id = "APS17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "APS",
	group = "Default",
	id = "APS18",
})

