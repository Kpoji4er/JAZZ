UndefineClass('MortarShell_Gas')
DefineClass.MortarShell_Gas = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	RepairCost = 0,
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/mortar_shell_gas",
	DisplayName = T(119056817440, "Газ. выстрел миномета"),
	DisplayNamePlural = T(334171064157, "Газ. выстрелы миномета"),
	Description = T(658584275546, "Газовый боеприпас для минометов."),
	AdditionalHint = T(217868623815, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>удушье</color>\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Выстрелы, совершенные сквозь облака газа, дают лишь незначительные попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Почти бесшумно"),
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

