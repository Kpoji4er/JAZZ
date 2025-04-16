UndefineClass('JAZZ_AMMO_38special')
DefineClass.JAZZ_AMMO_38special = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/38Sp.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special DisplayName]] ".38 Special"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special DisplayNamePlural]] ".38 Special"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special Description]] "Боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра .38 Special."),
	Cost = 10,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "44CAL",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_44CAL",
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

