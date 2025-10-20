UndefineClass('JAZZ_AMMO_30')
DefineClass.JAZZ_AMMO_30 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30cal.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30 DisplayName]] ".30 Cal"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30 DisplayNamePlural]] ".30 Cal"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30 Description]] "Боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра .38 Special."),
	Cost = 10,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "44CAL",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_30CAL",
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

