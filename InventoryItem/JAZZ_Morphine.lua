UndefineClass('JAZZ_Morphine')
DefineClass.JAZZ_Morphine = {
	__parents = { "JazzStackableMedicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "JazzStackableMedicine",
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_Morphine.png",
	DisplayName = T(890000000010014, "Morphine"),
	DisplayNamePlural = T(890000000010015, "Morphine"),
	AdditionalHint = T(890000000010016, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Morphine — suppresses Pain penalties\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Stabilizes and rallies downed characters (like a medkit)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Does not stop bleeding, restore HP, or heal trauma\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> No Medical skill required\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Self or ally"),
	Cost = 75,
	CanAppearInShop = true,
	RestockWeight = 75,
	MaxStock = 8,
	CategoryPair = "Medicine",
	MaxStacks = 10,
}
