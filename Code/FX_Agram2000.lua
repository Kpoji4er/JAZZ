PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Agram2000",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Agram2000_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxAgram2000",
})

PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "Agram2000",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Agram2000",
	group = "Weapons VFX",
	id = "FxAgram2000",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Agram2000",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxAgram20001",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Agram2000",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxAgram20002",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Agram2000",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxAgram20003",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M4Commando_reload",
	Source = "ActionPos",
	Target = "Agram2000",
	group = "Default",
	id = "fxAgram20004",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Agram2000",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M4Commando_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxAgram20005",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Agram2000",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxAgram20006",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "Agram2000",
	group = "Default",
	id = "fxAgram20007",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "Agram2000",
	group = "Default",
	id = "fxAgram20008",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Agram2000",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "M4Commando_reload",
	group = "Default",
	id = "fxAgram20009",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Agram2000",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxAgram200010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Agram2000",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxAgram200011",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "Agram2000",
	group = "Default",
	id = "fxAgram200012",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "Agram2000",
	group = "Default",
	id = "fxAgram200013",
})

