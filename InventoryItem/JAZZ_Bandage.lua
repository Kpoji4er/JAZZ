UndefineClass('JAZZ_Bandage')
DefineClass.JAZZ_Bandage = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "JazzStackableMedicine",
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Bandage.png",
	DisplayName = T(890000000010011, "Bandage"),
	DisplayNamePlural = T(890000000010012, "Bandages"),
	AdditionalHint = T(890000000010013, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage — reduce worst bleeding by one tier\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Low AP cost\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"),
	Cost = 25,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 150,
	MaxStock = 12,
	CategoryPair = "Medicine",
	MaxStacks = 30,
}
