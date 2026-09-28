UndefineClass('Medkit')
DefineClass.Medkit = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "JazzStackableMedicine",
	ScrapParts = 1,
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Medkit.png",
	DisplayName = T(890000000010025, --[[ModItemInventoryItemCompositeDef Medkit DisplayName]] "Medium Medkit"),
	DisplayNamePlural = T(890000000010026, --[[ModItemInventoryItemCompositeDef Medkit DisplayNamePlural]] "Medium Medkits"),
	AdditionalHint = T(890000000010027, --[[ModItemInventoryItemCompositeDef Medkit AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes one eligible medium or light trauma (eases combat penalties one tier; does not heal trauma)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP as % of max HP (scales with Medical: 18–60% from Medical 50 to 100)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Removes all bleeding\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Clears pain and wound infection; rallies downed\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack"),
	UnitStat = "Medical",
	Cost = 500,
	CanAppearInShop = true,
	RestockWeight = 80,
	CategoryPair = "Medicine",
	UsePriority = 1,
}

