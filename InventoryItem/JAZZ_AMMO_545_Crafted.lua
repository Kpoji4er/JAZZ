UndefineClass('JAZZ_AMMO_545_Crafted')
DefineClass.JAZZ_AMMO_545_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545Crafted.png",
	DisplayName = T(890000000000467, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Crafted DisplayName]] "5,45 мм, Кустарный"),
	DisplayNamePlural = T(890000000001223, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Crafted DisplayNamePlural]] "5,45 мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000001352, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Crafted Description]] "Заклинивший автомат калашникова больше не выдуманная история, используйте так, чтобы никто не видел."),
	Cost = 90,
	CanAppearInShop = false,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
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
			mod_add = 25,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

