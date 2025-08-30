PlaceObj('ActionFXInherit_Actor', {
	Actor = "MP5A2",
	Inherit = "MP5",
	group = "Weapons VFX",
	id = "fxMP5A2",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "MP5A4",
	Inherit = "MP5",
	group = "Weapons VFX",
	id = "fxMP5A4",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "MP5SD",
	Inherit = "MP5A4",
	group = "Weapons VFX",
	id = "fxMP5SD",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "MP5SD",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MP5SD",
	DetailLevel = 100,
	Moment = "start",
	Sound = "MP5SD_shot",
	Target = "Basic",
	group = "Default",
	id = "fxMP5SD",
})
