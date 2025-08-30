

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "MP446VIKING",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_shot",
	Target = "any",
	group = "Default",
	id = "fxPYA1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_equipncheck",
	Target = "Pistol",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxPYA",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "MP446VIKING",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "PYA",
	group = "Default",
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "PYA",
	group = "Default",
	id = "fxPYA",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "PYA_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "PYA",
	group = "Default",
	id = "fxPYA",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Delay = 500,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "PYA",
	group = "Default",
	id = "fxPYA",
})