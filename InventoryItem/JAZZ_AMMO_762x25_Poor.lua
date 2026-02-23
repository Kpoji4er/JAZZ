UndefineClass('JAZZ_AMMO_762x25_Poor')
DefineClass.JAZZ_AMMO_762x25_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x25Sub.png",
	DisplayName = T(527688384074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_Poor DisplayName]] "7.62x25, Lot 66-3 CN Substandard"),
	DisplayNamePlural = T(871962221654, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_Poor DisplayNamePlural]] "7.62x25, Lot 66-3 CN"),
	colorStyle = "AmmoBasicColor",
	Description = T(496628262702, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x25_Poor Description]] "Это самое отвратительное что вы можете вставить в своё оружие, если ты этим пользовался, я не хочу иметь с тобой дел."),
	Cost = 90,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 30,
	CategoryPair = "762x25",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_762x25",
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
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

