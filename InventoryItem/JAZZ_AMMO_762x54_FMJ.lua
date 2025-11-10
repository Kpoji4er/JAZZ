UndefineClass('JAZZ_AMMO_762x54_FMJ')
DefineClass.JAZZ_AMMO_762x54_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RLPS.png",
	DisplayName = T(685074706095, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_FMJ DisplayName]] "7,62x54R мм ЛПС (FMJ)"),
	DisplayNamePlural = T(544176135141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_FMJ DisplayNamePlural]] "7,62x54R мм ЛПС (FMJ)"),
	colorStyle = "AmmoBasicColor",
	Description = T(316044940928, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_FMJ Description]] "Советский винтовочный боеприпас калибра 7.62х54мм с пулей ЛПС"),
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 20,
	CategoryPair = "762x54",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "PenetrationBonus",
		}),
	},
}

