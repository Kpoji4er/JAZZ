-- Restore jazz M24 shot (was commented out in CodeSounds.lua).
-- Inheritors: ScoutSniper, ArcticWarfare, M700, FRF2 (via FX_M700.lua).
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "M24Sniper",
	Moment = "start",
	group = "Weapons VFX",
	id = "fxM24Sniper_remove_fire",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M24Sniper",
	DetailLevel = 100,
	Moment = "start",
	Sound = "M24Sniper_shot",
	Target = "any",
	group = "Default",
	id = "fxM24Sniper",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M24Sniper",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_sniper",
	Target = "Silencer",
	group = "Default",
	id = "fxM24Sniper_sil",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M24Sniper",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "fxM24Sniper_casing1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "M24Sniper",
	Delay = 400,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingC_fall",
	Source = "ActionPos",
	group = "Default",
	id = "fxM24Sniper_casing2",
})
