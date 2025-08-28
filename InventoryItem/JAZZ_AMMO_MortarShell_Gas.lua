UndefineClass('JAZZ_AMMO_MortarShell_Gas')
DefineClass.JAZZ_AMMO_MortarShell_Gas = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_gas",
	DisplayName = T(239000312996, "Газ. выстрел миномета"),
	DisplayNamePlural = T(191353195659, "Газ. выстрелы миномета"),
	Description = T(368317466121, "Газовый боеприпас для минометов."),
	AdditionalHint = T(203665951773, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>удушье</color>\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Выстрелы, совершенные сквозь облака газа, дают лишь незначительные попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Почти бесшумно"),
	Cost = 1800,
	Tier = 3,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "Ordnance",
	MaxStacks = 3,
	PenetrationClass = 1,
	BurnGround = false,
	Caliber = "JAZZ_Caliber_MortarShell",
	BaseDamage = 0,
	Noise = 0,
	aoeType = "toxicgas",
}

