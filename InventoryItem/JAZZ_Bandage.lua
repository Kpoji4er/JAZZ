UndefineClass('JAZZ_Bandage')
DefineClass.JAZZ_Bandage = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "JazzStackableMedicine",
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Bandage.png",
	DisplayName = T(890000000010011, --[[ModItemInventoryItemCompositeDef JAZZ_Bandage DisplayName]] "Bandage"),
	DisplayNamePlural = T(890000000010012, --[[ModItemInventoryItemCompositeDef JAZZ_Bandage DisplayNamePlural]] "Bandages"),
	AdditionalHint = T(890000000010013, --[[ModItemInventoryItemCompositeDef JAZZ_Bandage AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage — one use spends one bandage per bleed stack (up to your stock), each −1 tier\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> AP cost by Medical: 5 (0–19) / 4 (20–39) / 3 (40–59) / 2 (60–79) / 1 (80+)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"),
	Cost = 25,
	CanAppearInShop = true,
	MaxStock = 12,
	RestockWeight = 150,
	CategoryPair = "Medicine",
	MaxStacks = 30,
}

