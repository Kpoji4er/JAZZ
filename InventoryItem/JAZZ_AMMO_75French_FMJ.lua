UndefineClass('JAZZ_AMMO_75French_FMJ')
DefineClass.JAZZ_AMMO_75French_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/75.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ DisplayName]] "7,5х54 мм, Balle C (FMJ)"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ DisplayNamePlural]] "7,5х54 мм, Balle C (FMJ)"),
	colorStyle = "AmmoBasicColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_FMJ Description]] "Французский стандартный FMJ для 7.5×54 - стабильный и проверенный временем патрон для военных и гражданских задач."),
	Cost = 540,
	CanAppearInShop = true,
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

