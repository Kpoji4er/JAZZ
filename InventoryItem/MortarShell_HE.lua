UndefineClass('MortarShell_HE')
DefineClass.MortarShell_HE = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_he",
	DisplayName = T(155089126370, --[[ModItemInventoryItemCompositeDef MortarShell_HE DisplayName]] "Mortar Cartridge"),
	DisplayNamePlural = T(463883298336, --[[ModItemInventoryItemCompositeDef MortarShell_HE DisplayNamePlural]] "Mortar Cartridges"),
	colorStyle = "AmmoBasicColor",
	Description = T(544846349389, --[[ModItemInventoryItemCompositeDef MortarShell_HE Description]] "Explosive Ordnance ammo for Mortars."),
	Cost = 1600,
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	CenterObjDamageMod = 500,
	AreaOfEffect = 4,
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 70,
	AreaObjDamageMod = 200,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 120,
}

