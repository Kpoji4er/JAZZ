


PlaceObj('ActionFXInherit_Actor', {
	Actor = "G36c",
	Inherit = "G36",
	group = "Weapons VFX",
	id = "fxG36c",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "HK33",
	Inherit = "G36",
	group = "Weapons VFX",
	id = "fxHK33",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "HK33",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "HK33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HK33_shot",
	Target = "Basic",
	group = "Default",
	id = "fxHK33",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "HK33",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_rifle",
	Target = "Silencer",
	group = "Default",
	id = "fxHK33",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "G3A3",
	Inherit = "FNFAL",
	group = "Weapons VFX",
	id = "fxG3",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "G3A3",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "G3A3",
	DetailLevel = 100,
	Moment = "start",
	Sound = "G3_shot",
	Target = "Basic",
	group = "Default",
	id = "fxG3",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "G3A4",
	Inherit = "G3A3",
	group = "Weapons VFX",
	id = "fxG3",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "G3SniperV1",
	Inherit = "G3A3",
	group = "Weapons VFX",
	id = "fxG3",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig550",
	Inherit = "AUG",
	group = "Weapons VFX",
	id = "fxSig550",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Sig550",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Sig550_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSig550",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig550Custom",
	Inherit = "Sig550",
	group = "Weapons VFX",
	id = "fxSig550Custom",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig552",
	Inherit = "Sig550",
	group = "Weapons VFX",
	id = "fxSig552",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "Sig550",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "Sig550",
	DetailLevel = 100,
	Moment = "start",
	Sound = "Sig552_shot",
	Target = "Basic",
	group = "Default",
	id = "fxSig552",
})


PlaceObj('ActionFXInherit_Actor', {
	Actor = "Sig552SWAT",
	Inherit = "Sig552",
	group = "Weapons VFX",
	id = "fxSig552SWAT",
})

PlaceObj('ActionFXInherit_Actor', {
	Actor = "M21",
	Inherit = "M14SAW",
	group = "Weapons VFX",
	id = "fxM21",
})

PlaceObj('ActionFXRemove', {
	Action = "WeaponFire",
	Actor = "SKS",
	Moment = "start",
	group = "Weapons VFX",
	id = "8612833909699323100",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_shot",
	Target = "any",
	group = "Default",
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_equipncheck",
	Target = "SniperRifle",
	Source = "Camera",
	GameTime = true,
	group = "Default",
	id = "fxSKS",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Delay = 2200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Delay = 4200,
	Target = "Basic",
	group = "Default",
	GameTime = true,
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Source = "Camera",
	Target = "any",
	group = "Default",
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Source = "Camera",
	Delay = 4000,
	Target = "any",
	group = "Default",
	id = "fxSKS",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnjam",
	Actor = "SKS",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_reload",
	Source = "Camera",
	Delay = 4200,
	Target = "any",
	group = "Default",
	id = "fxSKS",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipin",
	Source = "Camera",
	Delay = 700,
	Target = "SKS",
	group = "Default",
	id = "fxSKS",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "SniperRifle",
	DetailLevel = 100,
	Moment = "start",
	Sound = "SKS_clipout",
	Source = "Camera",
	Delay = 0,
	Target = "SKS",
	group = "Default",
	id = "fxSKS",
})



PlaceObj('ActionFXInherit_Actor', {
	Actor = "M1A",
	Inherit = "M21",
	group = "Weapons VFX",
	id = "fxM1A",
})