UndefineClass('FirstAidKit')
DefineClass.FirstAidKit = {
	__parents = { "Medicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",
	object_class = "Medicine",
	ScrapParts = 1,
	Repairable = false,
	Icon = "Mod/e6L4ECj/Icons/Items/JAZZ_IFAK.png",
	DisplayName = T(890000000010022, "IFAK"),
	DisplayNamePlural = T(890000000010023, "IFAKs"),
	AdditionalHint = T(890000000010024, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores HP and stabilizes downed characters\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage action removes one worst bleeding stack\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Consumed on use; refill with Meds\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"),
	UnitStat = "Medical",
	Cost = 300,
	CanAppearInShop = true,
	RestockWeight = 150,
	CategoryPair = "Medicine",
	max_meds_parts = 10,
}
