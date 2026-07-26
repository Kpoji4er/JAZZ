UndefineClass('JAZZ_AMMO_30_P')
DefineClass.JAZZ_AMMO_30_P = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/30calHP.png",
	DisplayName = T(890000000001194, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_P DisplayName]] ".30 Cal M18 +P"),
	DisplayNamePlural = T(890000000000417, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_P DisplayNamePlural]] ".30 Cal M18 +P"),
	colorStyle = "AmmoHPColor",
	Description = T(890000000000276, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_30_P Description]] "Попытка сделать устаревший патрон бронебойным путем повышения давления. Уверенно справится с фанерой или кожанной курткой."),
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
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 700,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
	},
}

