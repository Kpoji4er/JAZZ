
--GrizzlyLAR
PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "GrizzlyLAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "50ae_shot",
	Target = "Basic",
	group = "Default",
	id = "fxGrizzlyLAR1",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "GrizzlyLAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "silencer_pistol",
	Target = "Silencer",
	group = "Default",
	id = "fxGrizzlyLAR2",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "GrizzlyLAR",
	Delay = 200,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_fall",
	Source = "ActionPos",
	group = "Default",
	id = "GrizzlyLAR3",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponFire",
	Actor = "GrizzlyLAR",
	Delay = 100,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "bullet_casingA_release",
	Source = "ActionPos",
	group = "Default",
	id = "GrizzlyLAR4",
})


PlaceObj('ActionFXParticles', {
	Action = "WeaponFire",
	Actor = "GrizzlyLAR",
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
	id = "GrizzlyLAR5",
})


PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "GrizzlyLAR",
	Time = 200,
	group = "Default",
	id = "GrizzlyLAR6",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 600,
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "GrizzlyLAR",
	group = "Default",
	id = "GrizzlyLAR7",
})

PlaceObj('ActionFXSound', {
	Action = "UnjamWeapon",
	Delay = 400,
	DetailLevel = 100,
	FadeOut = 50,
	Moment = "start",
	Sound = "HiPower_reload",
	Target = "GrizzlyLAR",
	Time = 200,
	group = "Default",
	id = "GrizzlyLAR8",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponEquip",
	Actor = "GrizzlyLAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "HiPower_reload",
	Source = "Camera",
	Target = "Pistol",
	group = "Default",
	id = "GrizzlyLAR9",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponJam",
	Actor = "GrizzlyLAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "empty_pistol",
	group = "Default",
	id = "GrizzlyLAR10",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "GrizzlyLAR",
	group = "Default",
	id = "GrizzlyLAR11",
})
 
PlaceObj('ActionFXSound', {
	Action = "WeaponLoad",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_load-9mm",
	Source = "Camera",
	Target = "GrizzlyLAR",
	group = "Default",
	id = "GrizzlyLAR12",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "GrizzlyLAR",
	Delay = 1700,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-load",
	group = "Default",
	id = "GrizzlyLAR13",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "GrizzlyLAR",
	Delay = 1300,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "HiPower_slide-move",
	group = "Default",
	id = "GrizzlyLAR14",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "GrizzlyLAR",
	Delay = 500,
	DetailLevel = 100,
	GameTime = true,
	Moment = "start",
	Sound = "mag_pistol-load",
	group = "Default",
	id = "GrizzlyLAR15",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponReload",
	Actor = "GrizzlyLAR",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	group = "Default",
	id = "GrizzlyLAR16",
})


PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	Delay = 700,
	DetailLevel = 100,
	Moment = "start",
	Sound = "bullet_unload-9mm",
	Source = "Camera",
	Target = "GrizzlyLAR",
	group = "Default",
	id = "GrizzlyLAR17",
})

PlaceObj('ActionFXSound', {
	Action = "WeaponUnload",
	Actor = "Pistol",
	DetailLevel = 100,
	Moment = "start",
	Sound = "mag_pistol-unload",
	Source = "Camera",
	Target = "GrizzlyLAR",
	group = "Default",
	id = "GrizzlyLAR18",
})

