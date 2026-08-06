UndefineClass('JAZZ_AMMO_9x18_FMJ')
DefineClass.JAZZ_AMMO_9x18_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18.png",
	DisplayName = T(890000000001198, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayName]] "9x18мм, ПСО FMJ"),
	DisplayNamePlural = T(890000000000421, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayNamePlural]] "9x18мм, ПСО FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000281, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ Description]] "Гражданский патрон для спортивной и охотничьей стрельбы, на кого охотятся с 9х18 надо ещё уточнить, но как минимум оружие будет стрелять исправно и возможно кто-то сегодня умрет."),
	Cost = 350,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 8,
	RestockWeight = 100,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
}

