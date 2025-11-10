UndefineClass('JAZZ_AMMO_46_FMJ')
DefineClass.JAZZ_AMMO_46_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/46.png",
	DisplayName = T(111421465880, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ DisplayName]] "4,6 мм, FMJ"),
	DisplayNamePlural = T(171557918481, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ DisplayNamePlural]] "4,6 мм, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(468404152064, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ Description]] "Базовый армейский патрон 4.6мм, для МП-7. Ни убавить ни прибавить, сочетает в себе легкий вес пули, дешевизну и наличие бронебойных свойств из-за своих размеров."),
	Cost = 600,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_46",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "CritChance",
		}),
	},
}

