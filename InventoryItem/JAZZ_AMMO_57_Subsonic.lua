UndefineClass('JAZZ_AMMO_57_Subsonic')
DefineClass.JAZZ_AMMO_57_Subsonic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/57sb.png",
	DisplayName = T(890000000000881, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_Subsonic DisplayName]] "5,7 мм, SB193 Дозвуковой"),
	DisplayNamePlural = T(890000000000254, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_Subsonic DisplayNamePlural]] "5,7 мм, SB193 Дозвуковой"),
	colorStyle = "AmmoSubsonicColor",
	Description = T(890000000001010, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_Subsonic Description]] "Дозвуковой патрон калибра 5.7, редкий и не очень нужный, однако если нужно работать швейной машинкой без шансов на обнаружение, это то что нужно. НЕ ЗАБУДЬТЕ НАДЕТЬ ГЛУШИТЕЛЬ !!!"),
	Cost = 1350,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 5,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_57",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 9,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -20,
			target_prop = "Noise",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "CritChance",
		}),
	},
}

