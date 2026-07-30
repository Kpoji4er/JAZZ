-- Wire unused Gewehr98_shot preset (bolt rifle; reload/jam reuse vanilla Gewehr98_*).
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Gewehr98",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxGewehr98_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Gewehr98",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_shot",
	Target = "any",
	group = "Default",
	id = "fxGewehr98",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Gewehr98",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_sniper",
	Target = "Silencer",
	group = "Default",
	id = "fxGewehr98_sil",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Gewehr98",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxGewehr98_casing1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Gewehr98",
	Delay = 400,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingC_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxGewehr98_casing2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Gewehr98",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_hammer-click",
	group = "Default",
	id = "fxGewehr98_jam",
})
