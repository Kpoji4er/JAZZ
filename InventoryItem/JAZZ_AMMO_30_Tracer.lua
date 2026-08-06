UndefineClass('JAZZ_AMMO_30_Tracer')
DefineClass.JAZZ_AMMO_30_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30calTracer.png",
	DisplayName = T(890000000001192, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer DisplayName]] ".30 Cal M27 Трассер"),
	DisplayNamePlural = T(890000000000415, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer DisplayNamePlural]] ".30 Cal M27 Трассер"),
	colorStyle = "AmmoTracerColor",
	Description = T(890000000000278, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer Description]] "Более современный армейский трассирующий вариант, современный ли? Как бы то ни было им можно выстрелить и даже попасть и помочь попасть другим"),
	Cost = 2100,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 45,
	CategoryPair = "44CAL",
	ShopStackSize = 120,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_30CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
	},
	AppliedEffects = {
		"ExposedMarkedTraccers",
	},
}

