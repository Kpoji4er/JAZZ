UndefineClass('JAZZ_AMMO_9x39_Crafted')
DefineClass.JAZZ_AMMO_9x39_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП6",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939Crafted.png",
	DisplayName = T(890000000000641, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted DisplayName]] "9x39 мм, Кустарный"),
	DisplayNamePlural = T(890000000000961, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted DisplayNamePlural]] "9x39 мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000000380, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted Description]] "Что-то среднее, между СП-5 и СП-6 собранное на коленке, как водится тут есть все минусы собранных на коленке патронов, возможно он даже не дозвуковой, проверяйте сами."),
	Cost = 80,
	CanAppearInShop = false,
	Tier = 3,
	MaxStock = 99,
	RestockWeight = 10,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
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
			mod_add = 20,
			target_prop = "CritChance",
		}),
	},
}

