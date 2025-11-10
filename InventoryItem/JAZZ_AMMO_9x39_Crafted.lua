UndefineClass('JAZZ_AMMO_9x39_Crafted')
DefineClass.JAZZ_AMMO_9x39_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП6",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939Crafted.png",
	DisplayName = T(508580108192, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted DisplayName]] "9x39 мм, Кустарный"),
	DisplayNamePlural = T(724138101974, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted DisplayNamePlural]] "9x39 мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(343666682437, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_Crafted Description]] "Вручную собранный патрон в кустарных условиях."),
	Cost = 900,
	Tier = 3,
	MaxStock = 99,
	RestockWeight = 10,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -25,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 200,
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
}

