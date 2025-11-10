UndefineClass('JAZZ_AMMO_762x39_APP')
DefineClass.JAZZ_AMMO_762x39_APP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/762x39API.png",
	DisplayName = T(333321938927, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_APP DisplayName]] "7,62х39мм, БЗ"),
	DisplayNamePlural = T(789710016757, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_APP DisplayNamePlural]] "7,62х39мм, БЗ"),
	colorStyle = "AmmoAPPColor",
	Description = T(527669776671, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_APP Description]] "Редкий бронебойно зажигательный патрон, мечта всех мужчин, которые держали в руках АКМ, это секс-бомба в мире патронов, ничего лучше вы уже в своей жизни не встретите."),
	Cost = 3000,
	CanAppearInShop = true,
	Tier = "5",
	MaxStock = 10,
	RestockWeight = 5,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			mod_mul = 0,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
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
			mod_add = 3,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Burning",
	},
}

