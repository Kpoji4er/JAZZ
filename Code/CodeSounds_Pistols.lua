-- Vanilla pistols with jazz shot presets that were never bound.

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Bereta92",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxBereta92_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Bereta92",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Bereta92_shot",
	Target = "any",
	group = "Default",
	id = "fxBereta92",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Bereta92",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxBereta92_sil",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "HiPower",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxHiPower_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "HiPower",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_shot",
	Target = "any",
	group = "Default",
	id = "fxHiPower",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "HiPower",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxHiPower_sil",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "DesertEagle",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxDesertEagle_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DesertEagle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "DesertEagle_shot",
	Target = "any",
	group = "Default",
	id = "fxDesertEagle",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "DesertEagle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxDesertEagle_sil",
})
