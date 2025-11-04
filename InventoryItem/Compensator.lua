UndefineClass('Compensator')
DefineClass.Compensator = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пока хз как раздуплить",
	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_muzzle",
	DisplayName = T(568412424587, "Компенсатор"),
	DisplayNamePlural = T(441080010376, "Компенсаторы"),
	AdditionalHint = T(431692419145, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Компенсатор. Можно поставить через экран модификаций"),
	Cost = 2900,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
}

