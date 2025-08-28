UndefineClass('OpticalLens')
DefineClass.OpticalLens = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/optical_lens",
	DisplayName = T(234015637580, "Линза"),
	DisplayNamePlural = T(869642347745, "Линзы"),
	AdditionalHint = T(421377090006, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется при создании улучшенных компонентов для оружия"),
	Cost = 3400,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
	MaxStacks = 500,
}

