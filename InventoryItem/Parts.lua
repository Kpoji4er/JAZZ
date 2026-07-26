UndefineClass('Parts')
DefineClass.Parts = {
	__parents = { "ResourceItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ResourceItem",
	Icon = "UI/Icons/Items/parts",
	DisplayName = T(807651722561, --[[ModItemInventoryItemCompositeDef Parts DisplayName]] "Parts"),
	DisplayNamePlural = T(476110713802, --[[ModItemInventoryItemCompositeDef Parts DisplayNamePlural]] "Parts"),
	AdditionalHint = T(683993796357, --[[ModItemInventoryItemCompositeDef Parts AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используются для модификации оружия\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используются для операции «Ремонт предметов» в виде со спутника."),
	Cost = 250,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "Resource",
	ShopStackSize = 5,
	MaxStacks = 5000,
}

