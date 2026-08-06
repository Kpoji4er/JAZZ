UndefineClass('JAZZ_AMMO_556_Tracer')
DefineClass.JAZZ_AMMO_556_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556T.png",
	DisplayName = T(653808281542, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Tracer DisplayName]] "5,56 мм, M856 Трассер"),
	DisplayNamePlural = T(493478127524, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Tracer DisplayNamePlural]] "5,56 мм, M856 Трассер"),
	colorStyle = "AmmoTracerColor",
	Description = T(816569867315, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Tracer Description]] "Армейские трассера проверенные временем, они нужны не столько для убийства, сколько для помощи другим в целеуказании, но что вам мешает пострелять по голожопым целям?"),
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 45,
	MaxStock = 5,
	CategoryPair = "556",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"ExposedMarkedTraccers",
	},
}

