-- Wire unused TexRevolver_shot; reload/handling reuse ColtAnaconda_* (closest revolver set).
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "TexRevolver",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxTexRevolver_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TexRevolver",
	DetailLevel = 100,
	Moment = "start",
	Sound = "TexRevolver_shot",
	Target = "Basic",
	group = "Default",
	id = "fxTexRevolver",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TexRevolver",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_revolver",
	Target = "Silencer",
	group = "Default",
	id = "fxTexRevolver_sil",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TexRevolver",
	DetailLevel = 100,
	Moment = "start",
	Sound = "ColtAnaconda_hammer-click",
	group = "Default",
	id = "fxTexRevolver_hammer",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "TexRevolver",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingB_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxTexRevolver_casing",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TexRevolver",
	DetailLevel = 100,
	Moment = "start",
	Sound = "ColtAnaconda_drum-open",
	group = "Default",
	GameTime = true,
	id = "fxTexRevolver_reload1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TexRevolver",
	Delay = 400,
	DetailLevel = 100,
	Moment = "start",
	Sound = "ColtAnaconda_casings-out",
	group = "Default",
	GameTime = true,
	id = "fxTexRevolver_reload2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TexRevolver",
	Delay = 900,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-45cal",
	group = "Default",
	GameTime = true,
	id = "fxTexRevolver_reload3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "TexRevolver",
	Delay = 1400,
	DetailLevel = 100,
	Moment = "start",
	Sound = "ColtAnaconda_drum-close",
	group = "Default",
	GameTime = true,
	id = "fxTexRevolver_reload4",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "TexRevolver",
	DetailLevel = 100,
	Moment = "start",
	Sound = "ColtAnaconda_cocking",
	Source = "Camera",
	Target = "Revolver",
	group = "Default",
	id = "fxTexRevolver_equip",
})
