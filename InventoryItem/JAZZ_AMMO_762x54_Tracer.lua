UndefineClass('JAZZ_AMMO_762x54_Tracer')
DefineClass.JAZZ_AMMO_762x54_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RTracer.png",
	DisplayName = T(351000794380, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer DisplayName]] "7,62x54R мм Т"),
	DisplayNamePlural = T(502291306563, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer DisplayNamePlural]] "7,62x54R мм Т"),
	colorStyle = "AmmoTracerColor",
	Description = T(556350640822, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Tracer Description]] "По сути базовый  патрон, но с трассирующей пулей, на случай необходимости сконцентрировать огонь отряда из ПКМ, ну а вдруг?"),
	Cost = 1260,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 20,
	RestockWeight = 10,
	CategoryPair = "762x54",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
	},
	AppliedEffects = {
		"ExposedMarkedTraccers",
	},
}

