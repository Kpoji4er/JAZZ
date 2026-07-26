UndefineClass('JAZZ_AMMO_556_AP')
DefineClass.JAZZ_AMMO_556_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556AP.png",
	DisplayName = T(890000000000349, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_AP DisplayName]] "5,56 мм, M995 Бронебойный"),
	DisplayNamePlural = T(890000000001316, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_AP DisplayNamePlural]] "5,56 мм, M995 Бронебойный"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000001003, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_AP Description]] "Серьезный бронебойный армейский боеприпас, крайне эффективен против брони любого класса защиты, скажи нет Джагернаутам!!! Дико дорого, но прекрасно."),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = "5",
	MaxStock = 5,
	RestockWeight = 5,
	CategoryPair = "556",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 6000,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
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
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Recoil",
		}),
	},
}

