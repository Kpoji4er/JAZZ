UndefineClass('JAZZ_AMMO_9x19_FMJ')
DefineClass.JAZZ_AMMO_9x19_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919FMJ.png",
	DisplayName = T(156976081814, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ DisplayName]] "9х19 мм, FMJ"),
	DisplayNamePlural = T(372328100854, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ DisplayNamePlural]] "9х19 мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(246192403774, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ Description]] "Стандартный патрон калибра 9х19мм"),
	Cost = 60,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {},
}

