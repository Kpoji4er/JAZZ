UndefineClass('JAZZ_AMMO_556_Crafted')
DefineClass.JAZZ_AMMO_556_Crafted = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556Crafted.png",
	DisplayName = T(890000000000739, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Crafted DisplayName]] "5,56мм, Кустарный"),
	DisplayNamePlural = T(890000000001038, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Crafted DisplayNamePlural]] "5,56 мм, Кустарный"),
	colorStyle = "AmmoCraftedColor",
	Description = T(890000000001055, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Crafted Description]] "Что будет, если на коленке собрать современный патрон, наплевав на всякие допуски? Правильно, он заклинит, отымеет ваше оружие и поможет отыметь вас, но у него хотя бы пуля не из бумаги..."),
	AdditionalHint = "",
	Cost = 200,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 50,
	CategoryPair = "556",
	ShopStackSize = 30,
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
	AppliedEffects = {
		"Bleeding",
	},
}

