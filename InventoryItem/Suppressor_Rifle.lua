UndefineClass('Suppressor_Rifle')
DefineClass.Suppressor_Rifle = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_muzzle",
	DisplayName = T(512280121443, --[[ModItemInventoryItemCompositeDef Suppressor_Rifle DisplayName]] "Компенсатор"),
	DisplayNamePlural = T(502809408099, --[[ModItemInventoryItemCompositeDef Suppressor_Rifle DisplayNamePlural]] "Компенсаторы"),
	AdditionalHint = T(826904154252, --[[ModItemInventoryItemCompositeDef Suppressor_Rifle AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Компенсатор, который можно поставить в оружие"),
	Cost = 2900,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
}

