UndefineClass('JAZZ_AMMO_45ACP_Crafted')
DefineClass.JAZZ_AMMO_45ACP_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPCrafted.png",
	DisplayName = T(890000000000239, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Crafted DisplayName]] ".45ACP, Кустарный"),
	DisplayNamePlural = T(890000000000054, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Crafted DisplayNamePlural]] ".45ACP, Кустарный"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000000860, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Crafted Description]] "Большой пистолетный патрон калибра .45, тут поддерживается дуализм, патрон по сути экспансивный, но и кустарный, а значит лизнуть мысли может как цели так и стрелку."),
	AdditionalHint = "",
	Cost = 60,
	CanAppearInShop = false,
	MaxStock = 50,
	CategoryPair = "45ACP",
	ShopStackSize = 50,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
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
	},
	AppliedEffects = {
		"Bleeding",
	},
}

