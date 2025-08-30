PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAT49",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MAT49_shot",
	Source = "ActionPos",
	Target = "Basic",
	group = "Default",
	id = "fxMAT49",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "MAT49",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "MAT49",
	group = "Weapons VFX",
	id = "FxMAT49",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAT49",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_submachine",
	Source = "ActionPos",
	Target = "Silencer",
	group = "Default",
	id = "fxMAT491",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAT49",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAT492",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MAT49",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAT493",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M14SAW_reload",
	Source = "ActionPos",
	Target = "MAT49",
	group = "Default",
	id = "fxMAT494",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "MAT49",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M14SAW_reload",
	Source = "Camera",
	Target = "SubmachineGun",
	group = "Default",
	id = "fxMAT495",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "MAT49",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_sniper",
	Source = "ActionPos",
	group = "Default",
	id = "fxMAT496",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "MAT49",
	group = "Default",
	id = "fxMAT497",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SubmachineGun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-load",
	Source = "Camera",
	Target = "MAT49",
	group = "Default",
	id = "fxMAT498",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAT49",
	Delay = 2000,
	DetailLevel = 100,
	FadeIn = 400,
	GameTime = true,
	Moment = "start",
	Sound = "M14SAW_reload",
	group = "Default",
	id = "fxMAT499",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAT49",
	Delay = 900,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-load",
	group = "Default",
	id = "fxMAT4910",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MAT49",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_submachine-unload",
	group = "Default",
	id = "fxMAT4911",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	Delay = 500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "MAT49",
	group = "Default",
	id = "fxMAT4912",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SubmachineGun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_submachine-unload",
	Source = "Camera",
	Target = "MAT49",
	group = "Default",
	id = "fxMAT4913",
})

