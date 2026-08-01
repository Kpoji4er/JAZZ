UndefineClass('JAZZ_AMMO_545_Tracer')
DefineClass.JAZZ_AMMO_545_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545T.png",
	DisplayName = T(965033233630, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer DisplayName]] "5,45 мм, 7Т3 Трассер"),
	DisplayNamePlural = T(430326314673, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer DisplayNamePlural]] "5,45 мм, 7Т3 Трассер"),
	colorStyle = "AmmoTracerColor",
	Description = T(212926171807, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Tracer Description]] "Если члены вашего отряда не видят куда стрелять, то данные трассирующие боеприпасы именно то что вам нужно, бонусом можете провернуть во враге горящую пулю."),
	AdditionalHint = "",
	Cost = 1050,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 2,
	RestockWeight = 10,
	CategoryPair = "545",
	ShopStackSize = 120,
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
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"ExposedBleedingChanceMarkedTraccers",
	},
}

