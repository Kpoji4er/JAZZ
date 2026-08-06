UndefineClass('Meds')
DefineClass.Meds = {
	__parents = { "ResourceItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ResourceItem",
	Icon = "UI/Icons/Items/medicine",
	DisplayName = T(182769023737, --[[ModItemInventoryItemCompositeDef Meds DisplayName]] "Meds"),
	DisplayNamePlural = T(186822751180, --[[ModItemInventoryItemCompositeDef Meds DisplayNamePlural]] "Meds"),
	AdditionalHint = T(834156151134, --[[ModItemInventoryItemCompositeDef Meds AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нужны для лечения ран на стратегической карте\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Расходуются в медицинских операциях и при крафте"),
	Cost = 100,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "Medicine",
	ShopStackSize = 5,
	MaxStacks = 5000,
}

