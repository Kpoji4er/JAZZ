UndefineClass('JAZZ_AMMO_762x39_Tracer')
DefineClass.JAZZ_AMMO_762x39_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39T.png",
	DisplayName = T(798317989173, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer DisplayName]] "7,62 мм СССР, ТРАС"),
	DisplayNamePlural = T(300974076449, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer DisplayNamePlural]] "7,62 мм СССР, ТРАС"),
	colorStyle = "AmmoTracerColor",
	Description = T(105546400626, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Tracer Description]] "Трассирующая версия армейского патрона, также как и базовый патрон хорош во всем в среднем по больнице, но тут вы становитесь душой коллектива!!!"),
	AdditionalHint = "",
	Cost = 1650,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 45,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
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
			mod_add = 30,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 990,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"ExposedMarkedTraccers",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

