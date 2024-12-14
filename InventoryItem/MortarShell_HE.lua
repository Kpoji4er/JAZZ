UndefineClass('MortarShell_HE')
DefineClass.MortarShell_HE = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_he",
	DisplayName = T(353521582405, --[[ModItemInventoryItemCompositeDef MortarShell_HE DisplayName]] "Выстрел для миномета"),
	DisplayNamePlural = T(237704902395, --[[ModItemInventoryItemCompositeDef MortarShell_HE DisplayNamePlural]] "Выстрелы для миномета"),
	colorStyle = "AmmoBasicColor",
	Description = T(657474544556, --[[ModItemInventoryItemCompositeDef MortarShell_HE Description]] "Стандартный боеприпас для минометов."),
	Cost = 1600,
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	CenterObjDamageMod = 500,
	AreaOfEffect = 2,
	AreaObjDamageMod = 500,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 120,
}

