UndefineClass('JAZZ_AMMO_MortarShell_HE')
DefineClass.JAZZ_AMMO_MortarShell_HE = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_he",
	DisplayName = T(756844134624, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE DisplayName]] "Выстрел для миномета"),
	DisplayNamePlural = T(587255830186, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE DisplayNamePlural]] "Выстрелы для миномета"),
	colorStyle = "AmmoBasicColor",
	Description = T(196674182820, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_HE Description]] "Стандартный боеприпас для минометов."),
	Cost = 1600,
	CanAppearInShop = true,
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
	BaseDamage = 40,
}

