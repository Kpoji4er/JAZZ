UndefineClass('JAZZ_AMMO_9x18_Crafted')
DefineClass.JAZZ_AMMO_9x18_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18Crafted.png",
	DisplayName = T(890000000001197, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Crafted DisplayName]] "9x18мм, Кустарный"),
	DisplayNamePlural = T(890000000000420, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Crafted DisplayNamePlural]] "9x18мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000000275, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Crafted Description]] "Патрон собранный на коленке, по известным причинам автор возможно умер, с этим боеприпасом вы опасны для всех и даже для себя."),
	Cost = 30,
	CanAppearInShop = false,
	MaxStock = 50,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Damage",
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
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

