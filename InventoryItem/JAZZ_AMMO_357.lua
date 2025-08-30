UndefineClass('JAZZ_AMMO_357')
DefineClass.JAZZ_AMMO_357 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/357_big.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357 DisplayName]] ".357 Magnum"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357 DisplayNamePlural]] ".357 Magnum"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357 Description]] "Боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра .38 Special."),
	Cost = 10,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "44CAL",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_357",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
	},
}

