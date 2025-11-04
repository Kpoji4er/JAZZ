UndefineClass('OilFilter')
DefineClass.OilFilter = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_muzzle",
	DisplayName = T(118793614826, --[[ModItemInventoryItemCompositeDef OilFilter DisplayName]] "Компенсатор"),
	DisplayNamePlural = T(735360883220, --[[ModItemInventoryItemCompositeDef OilFilter DisplayNamePlural]] "Компенсаторы"),
	AdditionalHint = T(409065182639, --[[ModItemInventoryItemCompositeDef OilFilter AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Компенсатор, который можно поставить в оружие"),
	Cost = 2900,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
}

