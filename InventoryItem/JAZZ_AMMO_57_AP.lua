UndefineClass('JAZZ_AMMO_57_AP')
DefineClass.JAZZ_AMMO_57_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/57AP.png",
	DisplayName = T(890000000000880, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_AP DisplayName]] "5,7 мм, S109 ББ"),
	DisplayNamePlural = T(890000000000253, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_AP DisplayNamePlural]] "5,7 мм, S109 ББ"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000001009, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_AP Description]] "Армейский бронебойный, он же и базовый патрон довольно редкого калибра. Пуля хоть и пистолетная, но эффективность практически как у автомата."),
	Cost = 2250,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_57",
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

