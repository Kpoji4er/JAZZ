UndefineClass('JAZZ_AMMO_9x18_AP')
DefineClass.JAZZ_AMMO_9x18_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18AP.png",
	DisplayName = T(890000000001199, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_AP DisplayName]] "9x18мм, ПСТ ББ"),
	DisplayNamePlural = T(890000000000422, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_AP DisplayNamePlural]] "9x18мм, ПСТ ББ"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000286, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_AP Description]] "Стандартный патрон 9х18 с повышенными характеристиками, может он и не такой убойный, но способен противостоять базовой бронезащите."),
	Cost = 810,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 850,
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
			mod_add = 3,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

