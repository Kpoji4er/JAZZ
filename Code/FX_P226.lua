PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P226",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol",
	Source = "Target",
	Spot = "Muzzle",
	Target = "P226",
	group = "Weapons VFX",
	id = "FxP226",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226",
	DetailLevel = 100,
	Moment = "start",
	Sound = "P226_shot",
	Target = "Basic",
	group = "Default",
	id = "fxP2261",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxP2262",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "P2263",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "P226",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "P2264",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "P226",
	Attach = true,
	GameTime = true,
	Moment = "start",
	Orientation = "SpotX",
	OrientationAxis = -1,
	Particles = "MuzzleFlash_Pistol_UpwardFlash",
	Source = "Target",
	Spot = "Muzzle",
	Target = "Compensator",
	group = "Weapons VFX",
	id = "P2265",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226",
	Time = 200,
	group = "Default",
	id = "P2266",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226",
	group = "Default",
	id = "P2267",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "P226",
	Time = 200,
	group = "Default",
	id = "P2268",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "P226",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "P2269",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "P226",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "P22610",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P226",
	group = "Default",
	id = "P22611",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "P226",
	group = "Default",
	id = "P22612",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "P22613",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "P22614",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "P22615",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "P226",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "P22616",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "P226",
	group = "Default",
	id = "P22617",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "P226",
	group = "Default",
	id = "P22618",
})