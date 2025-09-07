-----
PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxM1Garand",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_reload",
	Source = "Camera",
	Target = "SniperRifle",
	group = "Default",
	id = "fxM1Garand2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Garand_shot",
	Target = "any",
	group = "Default",
	id = "fxM1Garand3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M1Garand",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxM1Garand4",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M1Garand",
	Delay = 400,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingC_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxM1Garand5",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Gewehr98_hammer-click",
	group = "Default",
	id = "fxM1Garand6",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_equipncheck",
	Target = "SniperRifle",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxM1Garand7",
})

--[[
PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_clipout",
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM1Garand8",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_clipin",
	Delay = 2200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM1Garand9",
})
]]
PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_reload",
	Delay = 4200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxM1Garand10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M1Garand_equipncheck",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxM1Garand11",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "M1Garand",
	group = "Default",
	id = "fxM1Garand12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "M1Garand",
	group = "Default",
	id = "fxM1Garand13",
})