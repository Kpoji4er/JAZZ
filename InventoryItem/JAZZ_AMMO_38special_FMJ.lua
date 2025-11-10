UndefineClass('JAZZ_AMMO_38special_FMJ')
DefineClass.JAZZ_AMMO_38special_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/38Sp.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ DisplayName]] ".38 Special FMJ"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ DisplayNamePlural]] ".38 Special FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ Description]] "Стандартный патрон для дамских сверчков, мелкий револьверный патрон, нельзя носить россыпью, можно просто не нащупать в кармане."),
	Cost = 90,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "44CAL",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_38",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

