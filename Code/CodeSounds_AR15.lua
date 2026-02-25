

PlaceObj('ActionFXInherit_Actor', {
	Actor = "AR10",
	Inherit = "FNFAL",
	group = "Weapons VFX",
	id = "fxG3",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "AR10",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "AR10",
	DetailLevel = 100,
	Moment = "start",
	Sound = "G3_shot",
	Target = "Basic",
	group = "Default",
	id = "fxAR10",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "AR10DMR",
	Inherit = "AR10",
	group = "Weapons VFX",
	id = "fxAR10DMR",
})