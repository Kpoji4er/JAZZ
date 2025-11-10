UndefineClass('JAZZ_AMMO_762x25_AP')
DefineClass.JAZZ_AMMO_762x25_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x25ap.png",
	DisplayName = T(527688384074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_AP DisplayName]] "7.62x25, ПСТ (ББ)"),
	DisplayNamePlural = T(871962221654, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_AP DisplayNamePlural]] "7.62x25, ПСТ (ББ)"),
	colorStyle = "AmmoAPColor",
	Description = T(496628262702, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_AP Description]] "Бронебойный патрон 7.62х25, на самом деле он не бронебойный, но ничего лучше в данном калибре нету. Неплохо подходит для стрельбы в спину союзников."),
	Cost = 162,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "762x25",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_762x25",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
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
			mod_add = 5,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

