PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P90",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxP90",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P90",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "P90",
	group = "Weapons VFX",
	id = "FxP90",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P90",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxP901",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P90",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxP902",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P90",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxP903",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90reload",
	Source = "ActionPos",
	Target = "P90",
	group = "Default",
	id = "fxP904",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P90",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90equipncheck",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxP905",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P90",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxP906",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P90",
	group = "Default",
	id = "fxP907",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90clipin",
	Source = "Camera",
	Target = "P90",
	group = "Default",
	id = "fxP908",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P90",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "P90reload",
	group = "Default",
	id = "fxP909",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P90",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "P90clipin",
	group = "Default",
	id = "fxP9010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P90",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "P90clipout",
	group = "Default",
	id = "fxP9011",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P90",
	group = "Default",
	id = "fxP9012",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P90clipout",
	Source = "Camera",
	Target = "P90",
	group = "Default",
	id = "fxP9013",
})

