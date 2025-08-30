
PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "VSS",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_shot",
	Target = "any",
	group = "Default",
	id = "fxVSS1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_equipncheck",
	Target = "any",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxVSS",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipout",
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipin",
	Delay = 2200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_reload",
	Delay = 4200,
	Target = "any",
	group = "Default",
	GameTime = true,
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipin",
	Source = "Camera",
	Delay = 2200,
	Target = "any",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "VSS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "any",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "VSS",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "any",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "VSS",
	group = "Default",
	id = "fxVSS",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "any",
	DetailLevel = 100,
	Moment = "start",
	Sound = "VSS_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "VSS",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "any",
	DetailLevel = 100,
	Delay = 500,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "VSS",
	group = "Default",
	id = "fxVSS",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "AS_Val",
	Inherit = "VSS",
	group = "Weapons VFX",
	id = "VSS",
})
