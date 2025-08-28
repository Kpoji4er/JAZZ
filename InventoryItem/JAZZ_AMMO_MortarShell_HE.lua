UndefineClass('JAZZ_AMMO_MortarShell_HE')
DefineClass.JAZZ_AMMO_MortarShell_HE = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_he",
	DisplayName = T(574900180140, "Выстрел для миномета"),
	DisplayNamePlural = T(129650617617, "Выстрелы для миномета"),
	colorStyle = "AmmoBasicColor",
	Description = T(812608538603, "Стандартный боеприпас для минометов."),
	Cost = 1600,
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 3,
	CenterObjDamageMod = 500,
	AreaOfEffect = 2,
	AreaObjDamageMod = 500,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 120,
}

