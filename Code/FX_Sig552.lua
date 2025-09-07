
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig552",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SIG552_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSig552",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig552",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxSig5522",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig552",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxSig5523",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig552",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingB_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxSig5524",
})
PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	Moment = "start",
	Sound = "AUG_reload",
	Target = "Sig552",
	group = "Default",
	id = "fxSig5525",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "AUG_reload",
	Target = "Sig552",
	Time = 200,
	group = "Default",
	id = "fxSig5526",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Sig552",
	DetailLevel = 100,
	Moment = "start",
	Sound = "AUG_reload",
	Source = "Camera",
	Target = "AssaultRifle",
	group = "Default",
	id = "fxSig5527",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Sig552",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_submachine",
	group = "Default",
	id = "fxSig5528",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-556",
	Source = "Camera",
	Target = "Sig552",
	group = "Default",
	id = "fxSig5529",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 1300,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-load",
	Source = "Camera",
	Target = "Sig552",
	group = "Default",
	id = "fxSig55210",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig552",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "AUG_reload",
	group = "Default",
	id = "fxSig55211",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig552",
	Delay = 700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_rifle-load",
	group = "Default",
	id = "fxSig55212",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig552",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-unload",
	group = "Default",
	id = "fxSig55213",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 1000,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-556",
	Source = "Camera",
	Target = "Sig552",
	group = "Default",
	id = "fxSig55214",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-unload",
	Source = "Camera",
	Target = "Sig552",
	group = "Default",
	id = "fxSig55215",
})
PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig552SWAT",
	Inherit = "Sig552",
	group = "Weapons VFX",
	id = "fxSig552SWAT",
})