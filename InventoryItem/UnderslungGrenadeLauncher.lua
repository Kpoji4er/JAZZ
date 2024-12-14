UndefineClass('UnderslungGrenadeLauncher')
DefineClass.UnderslungGrenadeLauncher = {
	__parents = { "GrenadeLauncher" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "GrenadeLauncher",
	Reliability = 98,
	Caliber = "JAZZ_Caliber_40mmGrenade",
	AttackAP = 4000,
	Icon = "UI/Icons/Upgrades/m16_grenade_launcher",
	DisplayName = T(527844630900, --[[ModItemInventoryItemCompositeDef UnderslungGrenadeLauncher DisplayName]] "Подствол. гранатомет"),
	DisplayNamePlural = T(163578052946, --[[ModItemInventoryItemCompositeDef UnderslungGrenadeLauncher DisplayNamePlural]] "Подствол. гранатометы"),
	LargeItem = 1,
	UnitStat = "Explosives",
	Valuable = 1,
	Cost = 5000,
	CategoryPair = "HeavyWeapons",
	ObjDamageMod = 25,
	CritChanceScaled = 0,
	PenetrationClass = 2,
	WeaponRange = 45,
	HandSlot = "TwoHanded",
	fxClass = "MGL",
	PreparedAttackType = "None",
	ShootAP = 4000,
	ReloadAP = 3000,
	Handling = 60,
}

