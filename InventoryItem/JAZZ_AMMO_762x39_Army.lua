UndefineClass('JAZZ_AMMO_762x39_Army')
DefineClass.JAZZ_AMMO_762x39_Army = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/762x39PS.png",
	DisplayName = T(890000000000362, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Army DisplayName]] "7,62х39мм, ПС"),
	DisplayNamePlural = T(890000000001046, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Army DisplayNamePlural]] "7,62х39мм, ПС"),
	colorStyle = "AmmoArmyColor",
	Description = T(890000000000656, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Army Description]] "Базовый армейский патрон, по свойствам идеально сбалансирован на все случаи жизни. Это ширпотреб, в хорошем смысле этого слова. Берите не глядя, стреляйте не думая."),
	Cost = 840,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
	RestockWeight = 10,
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
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

