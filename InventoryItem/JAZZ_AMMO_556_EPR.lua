UndefineClass('JAZZ_AMMO_556_EPR')
DefineClass.JAZZ_AMMO_556_EPR = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556HP.png",
	DisplayName = T(326742931642, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_EPR DisplayName]] "5,56 мм, M855A1 Повышенной Пробиваемости"),
	DisplayNamePlural = T(946968976971, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_EPR DisplayNamePlural]] "5,56 мм, M855A1 Повышенной Пробиваемости"),
	colorStyle = "AmmoHPColor",
	Description = T(758340761081, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_EPR Description]] "Массовый армейский Повышенной Пробиваемости"),
	Cost = 2400,
	CanAppearInShop = true,
	Tier = "4",
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
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
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
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
	},
}

