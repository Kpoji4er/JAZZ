UndefineClass('JAZZ_AMMO_762x54_Crafted')
DefineClass.JAZZ_AMMO_762x54_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RCrafted.png",
	DisplayName = T(890000000000897, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted DisplayName]] "7,62x54R мм Кустарный"),
	DisplayNamePlural = T(890000000000689, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted DisplayNamePlural]] "7,62x54R мм Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000000331, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Crafted Description]] "Если уж делать хуже чем китайцы, то делать на коленке, плюс тут ровно один, приличный урон, но поплатитесь вы... Поверьте вы поплатитесь."),
	Cost = 60,
	CanAppearInShop = false,
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
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
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

