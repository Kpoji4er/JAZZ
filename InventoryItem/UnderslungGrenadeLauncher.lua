UndefineClass('UnderslungGrenadeLauncher')
DefineClass.UnderslungGrenadeLauncher = {
	__parents = { "GrenadeLauncher" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "GrenadeLauncher",
	Reliability = 98,
	MinMishapChance = -6,
	MaxMishapChance = 45,
	MaxMishapRange = 6,
	Caliber = "JAZZ_Caliber_40mmGrenade",
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(204366158384, --[[ModItemInventoryItemCompositeDef UnderslungGrenadeLauncher DisplayName]] "Underslung Launcher"),
	DisplayNamePlural = T(668594626073, --[[ModItemInventoryItemCompositeDef UnderslungGrenadeLauncher DisplayNamePlural]] "Underslung Launchers"),
	LargeItem = 1,
	UnitStat = "Explosives",
	Valuable = 1,
	Cost = 5000,
	CategoryPair = "HeavyWeapons",
	ObjDamageMod = 25,
	CritChanceScaled = 0,
	WeaponRange = 40,
	Noise = 30,
	HandSlot = "TwoHanded",
	fxClass = "MGL",
	PreparedAttackType = "None",
	AvailableAttacks = {
		"GrenadeLauncherFire",
	},
	ShootAP = 8000,
	ReloadAP = 8000,
	Handling = 58,
}

