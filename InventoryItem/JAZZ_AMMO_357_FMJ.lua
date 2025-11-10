UndefineClass('JAZZ_AMMO_357_FMJ')
DefineClass.JAZZ_AMMO_357_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/357.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_FMJ DisplayName]] ".357 Mag FMJ"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_FMJ DisplayNamePlural]] ".357 Mag FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_357_FMJ Description]] "Один из лучших револьверных патронов, не стареющая классика, хорош везде и всем."),
	Cost = 270,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "44CAL",
	ShopStackSize = 25,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_357",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "CritChance",
		}),
	},
}

