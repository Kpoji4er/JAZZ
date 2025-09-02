-----
PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Gewehr98",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Source = "Camera",
	Target = "SniperRifle",
	group = "Default",
	id = "fxSKS2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_shot",
	Target = "any",
	group = "Default",
	id = "fxSKS3",
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
	id = "fxSKS4",
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
	id = "fxSKS5",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "Gewehr98",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_hammer-click",
	group = "Default",
	id = "fxSKS6",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_equipncheck",
	Target = "SniperRifle",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxSKS7",
})

--[[
PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS8",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Delay = 2200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS9",
})
]]
PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Delay = 4200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxSKS11",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "SKS",
	group = "Default",
	id = "fxSKS12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "SKS",
	group = "Default",
	id = "fxSKS13",
})