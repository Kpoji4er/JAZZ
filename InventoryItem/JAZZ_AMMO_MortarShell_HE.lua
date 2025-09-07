UndefineClass('JAZZ_AMMO_MortarShell_HE')
DefineClass.JAZZ_AMMO_MortarShell_HE = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_he",
	DisplayName = T(574900180140, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE DisplayName]] "Выстрел для миномета"),
	DisplayNamePlural = T(129650617617, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE DisplayNamePlural]] "Выстрелы для миномета"),
	colorStyle = "AmmoBasicColor",
	Description = T(812608538603, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE Description]] "Стандартный боеприпас для минометов."),
	Cost = 1600,
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 3,
	CenterObjDamageMod = 500,
	AreaOfEffect = 6,
	CenterAreaOfEffect = 3,
	AreaUnitDamageMod = 20,
	AreaObjDamageMod = 250,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 120,
}

