UndefineClass('JAZZ_AMMO_556_Army')
DefineClass.JAZZ_AMMO_556_Army = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556M855.png",
	DisplayName = T(326742931642, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Army DisplayName]] "5,56 мм, M855 Армейский"),
	DisplayNamePlural = T(946968976971, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Army DisplayNamePlural]] "5,56 мм, M855 Армейский"),
	colorStyle = "AmmoArmyColor",
	Description = T(758340761081, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Army Description]] "Современный базовый армейский патрон, неплох во всём, вы точно не пожалеете.\n"),
	AdditionalHint = "",
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "556",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
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
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

