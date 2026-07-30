
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "DragunovSVD",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxDragunovSVD_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DragunovSVD",
	DetailLevel = 100,
	Moment = "start",
	Sound = "DragunovSVD_shot",
	Target = "any",
	group = "Default",
	id = "fxDragunovSVD",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "ZastavaM76",
	Inherit = "DragunovSVD",
	group = "Weapons VFX",
	id = "fxZastavaM76",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "ZastavaM76",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "ZastavaM76",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M76_shot",
	Target = "any",
	group = "Default",
	id = "fxZastavaM76",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "DragunovSVD_Custom",
	Inherit = "DragunovSVD",
	group = "Weapons VFX",
	id = "fxDragunovSVD_Custom",
})
