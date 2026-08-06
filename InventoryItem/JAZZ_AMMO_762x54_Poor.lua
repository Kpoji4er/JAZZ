UndefineClass('JAZZ_AMMO_762x54_Poor')
DefineClass.JAZZ_AMMO_762x54_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RPoor.png",
	DisplayName = T(890000000000895, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor DisplayName]] "7,62x54R мм 188-57 CN Type 53 Substandard"),
	DisplayNamePlural = T(890000000000687, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor DisplayNamePlural]] "7,62x54R мм 188-57 CN Type 53 Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000000332, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_Poor Description]] "Сделано в китае, нет ничего хуже, чем быть патроном, произведенным в китае."),
	Cost = 70,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 3,
	RestockWeight = 90,
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
			mod_add = -4,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 70,
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

