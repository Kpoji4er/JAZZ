UndefineClass('JAZZ_AMMO_3006_FMJ')
DefineClass.JAZZ_AMMO_3006_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "30-06",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/3006.png",
	DisplayName = T(697162729896, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_FMJ DisplayName]] "Патрон 30-06"),
	DisplayNamePlural = T(726631612816, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_FMJ DisplayNamePlural]] "Патроны 30-06"),
	colorStyle = "AmmoBasicColor",
	Description = T(898567748151, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_FMJ Description]] "Это папа калибра .308, патрон хоть и старый, но всё также опасен. Используется по сей день охотниками и ковбоями."),
	Cost = 540,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 1,
	CategoryPair = "3006",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_3006",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "PenetrationBonus",
		}),
	},
}

