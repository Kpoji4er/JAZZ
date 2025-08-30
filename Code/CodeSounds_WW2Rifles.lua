

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Mosin",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_shot",
	Target = "any",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_reload",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_equipncheck",
	Target = "SniperRifle",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltopen",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMosin",
})



PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltclose",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipin",
	Source = "Camera",
	Delay = 4000,
	Target = "any",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "Mosin",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltopen",
	Source = "Camera",
	Delay = 0,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltclose",
	Source = "Camera",
	Delay = 1200,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltopen",
	Source = "Camera",
	Delay = 0,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_clipout",
	Source = "Camera",
	Delay = 100,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mosin_boltclose",
	Source = "Camera",
	Delay = 0,
	Target = "Mosin",
	group = "Default",
	id = "fxMosin",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "SVT40",
	Inherit = "DragunovSVD",
	group = "Weapons VFX",
	id = "fxSVT40",
})
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "SVT40",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SVT40",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SVT40_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSVT40",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "AVT40",
	Inherit = "SVT40",
	group = "Weapons VFX",
	id = "fxAVT",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "BAR",
	Inherit = "MAC2429",
	group = "Weapons VFX",
	id = "fxBar",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "BAR",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "BAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Garand_shot",
	Target = "any",
	group = "Default",
	id = "fxBAR",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "Springfield",
	Inherit = "Gewehr98",
	group = "Weapons VFX",
	id = "fxBar",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Springfield",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Springfield",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Garand_shot",
	Target = "any",
	group = "Default",
	id = "fxSpringfield",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M1Garand",
	Inherit = "SKS",
	group = "Weapons VFX",
	id = "fxM1Garand",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "M1Garand",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M1Garand",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Garand_shot",
	Target = "any",
	group = "Default",
	id = "fxBAR",
})
