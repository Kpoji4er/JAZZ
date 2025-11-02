PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_reload",
	Source = "ActionPos",
	Target = "AA52",
	group = "Default",
	id = "fxAA52",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Delay = 1000,
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_machinegun-attach",
	Source = "Camera",
	Target = "AA52",
	group = "Default",
	id = "fxAA522",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_machinegun-detach",
	Source = "Camera",
	Target = "AA52",
	group = "Default",
	id = "fxAA523",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "AA52",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_DownwardVFlash",
	Source = "Target",
	Spot = "Muzzle",
	group = "Weapons VFX",
	id = "fxAA524",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "AA52",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_UpwardVFlash",
	Source = "Target",
	Spot = "Muzzle",
	group = "Weapons VFX",
	id = "fxAA525",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "AA52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_reload",
	Source = "Camera",
	Target = "MachineGun",
	group = "Default",
	id = "fxAA526",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AA52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "AA52_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxAA527",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AA52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_machinegun",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxAA528",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AA52",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxAA529",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AA52",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingC_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxAA5210",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "AA52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_machinegun",
	Source = "ActionPos",
	group = "Default",
	id = "fxAA5212",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "AA52",
	Delay = 3200,
	DetailLevel = 100,
	Moment = "start",
	Sound = "MG42_reload",
	group = "Default",
	id = "fxAA5213",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "AA52",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_machinegun-attach",
	group = "Default",
	id = "fxAA5214",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "AA52",
	Delay = 2600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_machinegun-close",
	group = "Default",
	id = "fxAA5215",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "AA52",
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_machinegun-open",
	group = "Default",
	id = "fxAA5216",
})