PlaceObj('ActionFXInherit_Actor', {
	Actor = "AKM",
	Inherit = "AK47",
	group = "Weapons VFX",
	id = "fxAKM",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "Type56",
	Inherit = "AK47",
	group = "Weapons VFX",
	id = "fxType56",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "AN94",
	Inherit = "AK74",
	group = "Weapons VFX",
	id = "fxAN94",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "AN94",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AN94",
	DetailLevel = 100,
	Moment = "start",
	Sound = "AN94_shot",
	Target = "Basic",
	group = "Default",
	id = "fxAN94",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "RPD",
	Inherit = "FNMinimi",
	group = "Weapons VFX",
	id = "fxRPD",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "RPD",
	Moment = "any",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "RPD",
	DetailLevel = 100,
	Moment = "any",
	Sound = "RPD_shot",
	Target = "any",
	group = "Default",
	id = "fxRPD",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "RPK",
	Inherit = "RPK74",
	group = "Weapons VFX",
	id = "fxRPK74",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "fxRPK",
	Moment = "any",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "RPK",
	DetailLevel = 100,
	Moment = "any",
	Sound = "RPK_shot",
	Target = "any",
	group = "Default",
	id = "fxfxRPK",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "Zastava_M70",
	Inherit = "AK47",
	group = "Weapons VFX",
	id = "fxZastavaM70",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "ZastavaM92",
	Inherit = "AKSU",
	group = "Weapons VFX",
	id = "fxZastavaM92",
})
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "ZastavaM92",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "ZastavaM92",
	DetailLevel = 100,
	Moment = "start",
	Sound = "ZastavaM92_shot",
	Target = "Basic",
	group = "Default",
	id = "fxZastavaM92",
})
