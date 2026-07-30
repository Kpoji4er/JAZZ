
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Striker_shot",
	Target = "Basic",
	group = "Default",
	id = "fxStriker",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxStriker2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Striker",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxStriker3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Striker",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingSHOTGUN_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxStriker4",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 1000,
	DetailLevel = 100,
	Moment = "start",
	Sound = "AA12_reload",
	Target = "Striker",
	group = "Default",
	id = "fxStriker5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeIn = 100,
	Moment = "start",
	Sound = "AA12_reload",
	Target = "Striker",
	Time = 300,
	group = "Default",
	id = "fxStriker6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeIn = 100,
	Moment = "start",
	Sound = "AA12_reload",
	Target = "Striker",
	Time = 300,
	group = "Default",
	id = "fxStriker7",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponAutoFire",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	-- AA12_shot_auto preset missing; reuse Single samples (same AA12 dry pack)
	Sound = "AA12_shot_Single",
	Target = "Basic",
	group = "Default",
	id = "fxStriker8",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponAutoFire",
	Actor = "Striker",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingSHOTGUN_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxStriker9",
})



PlaceObj('ActionFXSound', {
	Action = "WeaponBuckshot",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Striker_shot",
	Target = "Basic",
	group = "Default",
	id = "fxStriker10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponBuckshot",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxStriker11",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponBuckshot",
	Actor = "Striker",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxStriker12",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponBuckshot",
	Actor = "Striker",
	Delay = 300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingSHOTGUN_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxStriker13",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "AA12_reload",
	Source = "Camera",
	Target = "Shotgun",
	group = "Default",
	id = "fxStriker14",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_rifle",
	group = "Default",
	id = "fxStriker15",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Shotgun",
	Delay = 1500,
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_box-attach",
	Source = "Camera",
	Target = "Striker",
	group = "Default",
	id = "fxStriker16",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Shotgun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-12gauge-mag",
	Source = "Camera",
	Target = "Striker",
	group = "Default",
	id = "fxStriker17",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Striker",
	Delay = 2700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "AA12_reload",
	group = "Default",
	id = "fxStriker18",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Striker",
	Delay = 2000,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "belt_box-attach",
	group = "Default",
	id = "fxStriker19",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Striker",
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_box-detach",
	group = "Default",
	id = "fxStriker20",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Striker",
	Delay = 800,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_load-12gauge-mag",
	group = "Default",
	id = "fxStriker21",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Shotgun",
	DetailLevel = 100,
	Moment = "start",
	Sound = "belt_box-detach",
	Source = "Camera",
	Target = "Striker",
	group = "Default",
	id = "fxStriker22",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Shotgun",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-12gauge-mag",
	Source = "Camera",
	Target = "Striker",
	group = "Default",
	id = "fxStriker23",
})
