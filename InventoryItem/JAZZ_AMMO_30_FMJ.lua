UndefineClass('JAZZ_AMMO_30_FMJ')
DefineClass.JAZZ_AMMO_30_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30cal.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ DisplayName]] ".30 Cal M1 Ball"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ DisplayNamePlural]] ".30 Cal M1 Ball"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ Description]] "Вроде это армейский образец, но это не точно, он на столько стар, что его просто продают ведрами вместе с другими старыми патронами."),
	Cost = 360,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 1,
	CategoryPair = "44CAL",
	ShopStackSize = 120,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_30CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			mod_mul = 0,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

