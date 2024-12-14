UndefineClass('JAZZ_AMMO_57_FMJ')
DefineClass.JAZZ_AMMO_57_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/57.png",
	DisplayName = T(674003227379, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_FMJ DisplayName]] "5,7 мм, S109"),
	DisplayNamePlural = T(278698960462, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_FMJ DisplayNamePlural]] "5,7 мм, S109"),
	colorStyle = "AmmoBasicColor",
	Description = T(761420797793, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_FMJ Description]] "Боеприпас калибра 5.7мм"),
	AdditionalHint = T(246724665120, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_57_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	CategoryPair = "57",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_57",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

