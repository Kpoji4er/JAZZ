--PB
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Basic",
	group = "Default",
	id = "fxPB1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxPB2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PB",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "PB3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PB",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "PB4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "PB",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_Silencer",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Compensator",
	group = "Weapons VFX",
	id = "PB5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxPB1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxPB2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxPB3",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_equipncheck",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "PB9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "PB10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "PB",
	group = "Default",
	id = "PB11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "PB",
	group = "Default",
	id = "PB12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPB13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPB14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "PB",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PB_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPB15",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "PB",
	group = "Default",
	id = "PB17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "PB",
	group = "Default",
	id = "PB18",
})

