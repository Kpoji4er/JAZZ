UndefineClass('JAZZ_AMMO_9x18_FMJ')
DefineClass.JAZZ_AMMO_9x18_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayName]] "9x18мм, обычный"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayNamePlural]] "9x18мм, обычный"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ Description]] "Боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра 9x18 мм."),
	Cost = 30,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "9x18",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "PenetrationClass",
		}),
	},
}

