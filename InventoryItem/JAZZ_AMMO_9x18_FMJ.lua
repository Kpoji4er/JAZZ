UndefineClass('JAZZ_AMMO_9x18_FMJ')
DefineClass.JAZZ_AMMO_9x18_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayName]] "9x18мм, ПСО FMJ"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ DisplayNamePlural]] "9x18мм, ПСО FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_FMJ Description]] "Гражданский патрон для спортивной и охотничьей стрельбы, на кого охотятся с 9х18 надо ещё уточнить, но как минимум оружие будет стрелять исправно и возможно кто-то сегодня умрет."),
	Cost = 240,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 20,
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

