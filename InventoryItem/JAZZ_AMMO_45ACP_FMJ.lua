UndefineClass('JAZZ_AMMO_45ACP_FMJ')
DefineClass.JAZZ_AMMO_45ACP_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACP.png",
	DisplayName = T(270886313378, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayName]] ".45ACP, FMJ"),
	DisplayNamePlural = T(136983924045, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ DisplayNamePlural]] ".45ACP, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(654722607287, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_FMJ Description]] "Стандартный патрон калибра .45ACP"),
	AdditionalHint = "",
	Cost = 60,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "45ACP",
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_45ACP",
}

