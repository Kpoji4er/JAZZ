UndefineClass('JAZZ_AMMO_75French_FMJ')
DefineClass.JAZZ_AMMO_75French_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/75.png",
	DisplayName = T(890000000000133, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ DisplayName]] "7,5х54 мм, Balle C (FMJ)"),
	DisplayNamePlural = T(890000000001058, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ DisplayNamePlural]] "7,5х54 мм, Balle C (FMJ)"),
	colorStyle = "AmmoBasicColor",
	Description = T(890000000000828, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ Description]] "Что-то на французском, вроде как базовый патрон, но пенетрирует не хуже некоторых бронебойных, жаль оружие под него вышло в тираж."),
	Cost = 200,
	CanAppearInShop = false,
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "792",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_75French",
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

