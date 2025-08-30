--Makarov
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "TT33_shot",
	Target = "Basic",
	group = "Default",
	id = "fxCZ521",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxCZ522",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ52",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "CZ523",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "CZ52",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "CZ524",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "CZ52",
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
	id = "CZ525",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxCZ521",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxCZ522",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxCZ523",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_equipncheck",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "CZ529",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "CZ5210",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "CZ52",
	group = "Default",
	id = "CZ5211",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "CZ52",
	group = "Default",
	id = "CZ5212",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxCZ5213",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxCZ5214",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "CZ52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxCZ5215",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "CZ52",
	group = "Default",
	id = "CZ5217",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "CZ52",
	group = "Default",
	id = "CZ5218",
})

