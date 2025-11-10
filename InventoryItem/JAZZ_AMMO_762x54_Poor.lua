UndefineClass('JAZZ_AMMO_762x54_Poor')
DefineClass.JAZZ_AMMO_762x54_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RSub.png",
	DisplayName = T(685074706095, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor DisplayName]] "7,62x54R мм 188-57 CN Type 53 Substandard"),
	DisplayNamePlural = T(544176135141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor DisplayNamePlural]] "7,62x54R мм 188-57 CN Type 53 Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(316044940928, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor Description]] "Старый сурплюсный патрон - дёшево и массово в коллекциях и запасах. Работает, но уступает по кучности современным аналогам."),
	Cost = 750,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 30,
	CategoryPair = "762x54",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 100,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
	},
}

