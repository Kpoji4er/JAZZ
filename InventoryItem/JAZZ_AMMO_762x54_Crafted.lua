UndefineClass('JAZZ_AMMO_762x54_Crafted')
DefineClass.JAZZ_AMMO_762x54_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RCrafted.png",
	DisplayName = T(685074706095, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted DisplayName]] "7,62x54R мм Кустарный"),
	DisplayNamePlural = T(544176135141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted DisplayNamePlural]] "7,62x54R мм Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(316044940928, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted Description]] "Кустарный"),
	Cost = 240,
	Tier = 2,
	MaxStock = 5,
	CategoryPair = "762x54",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -25,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 200,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
	},
}

