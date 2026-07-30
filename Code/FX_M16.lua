PlaceObj('ActionFXInherit_Actor', {
	Actor = "M16A1",
	Inherit = "M16A2",
	group = "Weapons VFX",
	id = "fxM16A1",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M16A4",
	Inherit = "M16A2",
	group = "Weapons VFX",
	id = "fxM16A4",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "Mini14",
	Inherit = "M16A2",
	group = "Weapons VFX",
	id = "fxMini14",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Mini14",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxMini14_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Mini14",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Mini14_shot",
	Target = "any",
	group = "Default",
	id = "fxMini14_shot",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "M4A1",
	Inherit = "M4Commando",
	group = "Weapons VFX",
	id = "fxM4A1",
})
