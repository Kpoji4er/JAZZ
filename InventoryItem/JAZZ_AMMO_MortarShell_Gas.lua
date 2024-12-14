UndefineClass('JAZZ_AMMO_MortarShell_Gas')
DefineClass.JAZZ_AMMO_MortarShell_Gas = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_gas",
	DisplayName = T(475771289620, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_Gas DisplayName]] "Газ. выстрел миномета"),
	DisplayNamePlural = T(979643566872, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_Gas DisplayNamePlural]] "Газ. выстрелы миномета"),
	Description = T(627453516049, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_Gas Description]] "Газовый боеприпас для минометов."),
	AdditionalHint = T(100940450195, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_MortarShell_Gas AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>удушье</color>\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Выстрелы, совершенные сквозь облака газа, дают лишь незначительные попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Почти бесшумно"),
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	PenetrationClass = 1,
	BurnGround = false,
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 0,
	Noise = 0,
	aoeType = "toxicgas",
}

