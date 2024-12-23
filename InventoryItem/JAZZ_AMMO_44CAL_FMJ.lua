UndefineClass('JAZZ_AMMO_44CAL_FMJ')
DefineClass.JAZZ_AMMO_44CAL_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44FMJ.png",
	DisplayName = T(283758588700, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ DisplayName]] ".44, FMJ"),
	DisplayNamePlural = T(124552577193, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ DisplayNamePlural]] ".44, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(472698757891, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ Description]] "Стандартный патрон для револьверов и винтовок калибра .44."),
	AdditionalHint = T(985517357738, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 40,
	CanAppearInShop = true,
	MaxStock = 50,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
}

