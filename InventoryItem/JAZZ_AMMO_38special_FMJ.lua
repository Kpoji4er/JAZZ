UndefineClass('JAZZ_AMMO_38special_FMJ')
DefineClass.JAZZ_AMMO_38special_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/38Sp.png",
	DisplayName = T(890000000001190, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ DisplayName]] ".38 Special FMJ"),
	DisplayNamePlural = T(890000000000413, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ DisplayNamePlural]] ".38 Special FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000284, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_38special_FMJ Description]] "Стандартный патрон для дамских сверчков, мелкий револьверный патрон, нельзя носить россыпью, можно просто не нащупать в кармане."),
	Cost = 400,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 8,
	RestockWeight = 100,
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

