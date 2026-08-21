UndefineClass('JAZZ_AMMO_30_FMJ')
DefineClass.JAZZ_AMMO_30_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30cal.png",
	DisplayName = T(890000000001193, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ DisplayName]] ".30 Cal M1 Ball"),
	DisplayNamePlural = T(890000000000416, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ DisplayNamePlural]] ".30 Cal M1 Ball"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000280, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_FMJ Description]] "Вроде это армейский образец, но это не точно, он на столько стар, что его просто продают ведрами вместе с другими старыми патронами."),
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 8,
	RestockWeight = 100,
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
			target_prop = "PenetrationBonus",
		}),
	},
}

