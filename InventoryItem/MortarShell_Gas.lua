UndefineClass('MortarShell_Gas')
DefineClass.MortarShell_Gas = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_gas",
	DisplayName = T(695814790332, --[[ModItemInventoryItemCompositeDef MortarShell_Gas DisplayName]] "Mortar Gas Cartridge"),
	DisplayNamePlural = T(485162600133, --[[ModItemInventoryItemCompositeDef MortarShell_Gas DisplayNamePlural]] "Mortar Gas Cartridges"),
	Description = T(866167485518, --[[ModItemInventoryItemCompositeDef MortarShell_Gas Description]] "Ordnance ammo for Mortars."),
	AdditionalHint = T(217868623815, --[[ModItemInventoryItemCompositeDef MortarShell_Gas AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>удушье</color>\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Выстрелы, совершенные сквозь облака газа, дают лишь незначительные попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Почти бесшумно"),
	Cost = 1800,
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

