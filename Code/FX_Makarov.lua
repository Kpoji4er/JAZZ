--Makarov
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_shot",
	Target = "Basic",
	group = "Default",
	id = "fxMakarov1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxMakarov2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Makarov",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "Makarov3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Makarov",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "Makarov4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Makarov",
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
	id = "Makarov5",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxMakarov1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxMakarov2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxMakarov3",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_equipncheck",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "Makarov9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "Makarov10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Makarov",
	group = "Default",
	id = "Makarov11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Makarov",
	group = "Default",
	id = "Makarov12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMakarov13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMakarov14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Makarov",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Makarov_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMakarov15",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Makarov",
	group = "Default",
	id = "Makarov17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "Makarov",
	group = "Default",
	id = "Makarov18",
})

