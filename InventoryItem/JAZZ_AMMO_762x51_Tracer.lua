UndefineClass('JAZZ_AMMO_762x51_Tracer')
DefineClass.JAZZ_AMMO_762x51_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM62.png",
	DisplayName = T(170269301418, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Tracer DisplayName]] "7.62х51мм НАТО, M62"),
	DisplayNamePlural = T(970505261363, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Tracer DisplayNamePlural]] "7.62х51мм НАТО, M62"),
	colorStyle = "AmmoTracerColor",
	Description = T(964415083636, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Tracer Description]] "Трассирующий вариант стандартного М80, с амбициями на бронебойность. На деле же амбиции как всегда завышены, но он правда эффективен."),
	AdditionalHint = "",
	Cost = 2100,
	CanAppearInShop = true,
	Tier = "4",
	MaxStock = 10,
	RestockWeight = 5,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

