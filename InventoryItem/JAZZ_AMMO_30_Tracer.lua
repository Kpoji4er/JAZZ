UndefineClass('JAZZ_AMMO_30_Tracer')
DefineClass.JAZZ_AMMO_30_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30caltracer.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer DisplayName]] ".30 Cal M27 Трассер"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer DisplayNamePlural]] ".30 Cal M27 Трассер"),
	colorStyle = "AmmoTracerColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_Tracer Description]] "Более современный армейский трассирующий вариант, современный ли? Как бы то ни было им можно выстрелить и даже попасть и помочь попасть другим"),
	Cost = 540,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 1,
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
			mod_add = 2,
			target_prop = "CritChance",
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
		"Exposed",
	},
}

