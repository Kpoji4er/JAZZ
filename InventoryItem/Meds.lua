UndefineClass('Meds')
DefineClass.Meds = {
	__parents = { "ResourceItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ResourceItem",
	Icon = "UI/Icons/Items/medicine",
	DisplayName = T(658657633995, "Медикаменты"),
	DisplayNamePlural = T(587879132073, "Медикаменты"),
	AdditionalHint = T(834156151134, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используются для операции «Лечение ран» в виде со спутника\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используются для восполнения аптечек и наборов первой помощи"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "Medicine",
	ShopStackSize = 5,
	MaxStacks = 5000,
}

