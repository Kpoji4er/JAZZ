UndefineClass('JAZZ_AMMO_9x19_Crafted')
DefineClass.JAZZ_AMMO_9x19_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919Crafted.png",
	DisplayName = T(890000000000078, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Crafted DisplayName]] "9х19 мм, Кустарные"),
	DisplayNamePlural = T(890000000000436, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Crafted DisplayNamePlural]] "9х19 мм, Кустарные"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000000196, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Crafted Description]] "Производитель не известен, возможно это вы сами, рекомендуется использовать с оружием которое вы ненавидите, тогда эти патроны помогут вам скорее от него избавиться. Сильно снижают надежность оружия."),
	Cost = 60,
	CanAppearInShop = false,
	MaxStock = 50,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -18,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 140,
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
	AppliedEffects = {
		"Bleeding",
	},
}

