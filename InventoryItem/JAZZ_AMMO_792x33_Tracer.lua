UndefineClass('JAZZ_AMMO_792x33_Tracer')
DefineClass.JAZZ_AMMO_792x33_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/792x33Tracer.png",
	DisplayName = T(890000000000363, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_Tracer DisplayName]] "792x33мм L'spur Трассер"),
	DisplayNamePlural = T(890000000001047, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_Tracer DisplayNamePlural]] "792x33мм L'spur Трассер"),
	colorStyle = "AmmoTracerColor",
	Description = T(890000000000658, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792x33_Tracer Description]] "Версия патрона с трассером, иными словами прокладывающий путь к душам и сердцам по ту сторону ствола, патрон старый, но светит всё также.... кажется."),
	AdditionalHint = "",
	Cost = 675,
	CanAppearInShop = true,
	MaxStock = 10,
	RestockWeight = 1,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_792x33",
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

