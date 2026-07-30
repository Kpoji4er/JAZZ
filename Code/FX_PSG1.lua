-- PSG1 is G3-family; inherit reload/VFX from G3A3, override fire with unused PSG1_shot.
PlaceObj('ActionFXInherit_Actor', {
	Actor = "PSG1",
	Inherit = "G3A3",
	group = "Weapons VFX",
	id = "fxPSG1",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "PSG1",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxPSG1_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PSG1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PSG1_shot",
	Target = "any",
	group = "Default",
	id = "fxPSG1_shot",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "PSG1",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxPSG1_sil",
})
