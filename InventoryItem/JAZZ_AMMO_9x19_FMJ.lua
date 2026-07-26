UndefineClass('JAZZ_AMMO_9x19_FMJ')
DefineClass.JAZZ_AMMO_9x19_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919FMJ.png",
	DisplayName = T(890000000000080, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ DisplayName]] "9х19 мм, Luger FMJ"),
	DisplayNamePlural = T(890000000000438, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ DisplayNamePlural]] "9х19 мм, Luger FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000197, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_FMJ Description]] "Заводской патрон 9х19, ни больше ни меньше, можно стрелять по не бронированным целям без опасений, что вам выбьет глаз затвором."),
	Cost = 300,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 20,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
	},
}

