UndefineClass('JAZZ_AMMO_792_FMJ')
DefineClass.JAZZ_AMMO_792_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/792x57.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ DisplayName]] "7,92х57 мм, s.S. Patrone (FMJ)"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ DisplayNamePlural]] "7,92х57 мм, s.S. Patrone (FMJ)"),
	colorStyle = "AmmoBasicColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ Description]] "Плотная полнооболочечная конструкция для 7.92 - исторический боевой стандарт с приличной кучностью."),
	AdditionalHint = "",
	Cost = 540,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "792",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_792",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
	},
}

