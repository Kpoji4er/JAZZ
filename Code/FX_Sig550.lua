
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SIG550_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSig550",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxSig5502",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxSig5503",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingB_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxSig5504",
})
PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	Moment = "start",
	Sound = "AUG_reload",
	Target = "Sig550",
	group = "Default",
	id = "fxSig5505",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "AUG_reload",
	Target = "Sig550",
	Time = 200,
	group = "Default",
	id = "fxSig5506",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "AUG_reload",
	Source = "Camera",
	Target = "AssaultRifle",
	group = "Default",
	id = "fxSig5507",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_submachine",
	group = "Default",
	id = "fxSig5508",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-556",
	Source = "Camera",
	Target = "Sig550",
	group = "Default",
	id = "fxSig5509",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "AssaultRifle",
	Delay = 1300,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-load",
	Source = "Camera",
	Target = "Sig550",
	group = "Default",
	id = "fxSig55010",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig550",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "AUG_reload",
	group = "Default",
	id = "fxSig55011",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig550",
	Delay = 700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_rifle-load",
	group = "Default",
	id = "fxSig55012",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-unload",
	group = "Default",
	id = "fxSig55013",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 1000,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-556",
	Source = "Camera",
	Target = "Sig550",
	group = "Default",
	id = "fxSig55014",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "AssaultRifle",
	Delay = 100,
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_rifle-unload",
	Source = "Camera",
	Target = "Sig550",
	group = "Default",
	id = "fxSig55015",
})
PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig550Custom",
	Inherit = "Sig550",
	group = "Weapons VFX",
	id = "fxSig550Custom",
})