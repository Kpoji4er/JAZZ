UndefineClass('JAZZ_AMMO_9x19_Poor')
DefineClass.JAZZ_AMMO_9x19_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919Substandart.png",
	DisplayName = T(890000000000079, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Poor DisplayName]] "9х19 мм, 9mm Ball Substandard"),
	DisplayNamePlural = T(890000000000437, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Poor DisplayNamePlural]] "9х19 мм, 9mm Ball Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000000198, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Poor Description]] "Это как стрелять из огнестрельного оружия шариками из жеваной бумаги, из плюсов можно выделить то, что это очень дешево и много. \nСтабильная работа не гарантируется, кучность тоже, а ещё размокшая жеваная бумага может быстро засрать ваше оружие."),
	Cost = 150,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 3,
	RestockWeight = 90,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 120,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
}

