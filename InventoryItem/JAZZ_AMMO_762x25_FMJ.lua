UndefineClass('JAZZ_AMMO_762x25_FMJ')
DefineClass.JAZZ_AMMO_762x25_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x25.png",
	DisplayName = T(527688384074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ DisplayName]] "7.62x25, обычный"),
	DisplayNamePlural = T(871962221654, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ DisplayNamePlural]] "7.62x25, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(496628262702, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_FMJ Description]] "Боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра 7.62x25, "),
	Cost = 30,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "762x25",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_762x25",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
}

