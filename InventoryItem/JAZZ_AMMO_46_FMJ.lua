UndefineClass('JAZZ_AMMO_46_FMJ')
DefineClass.JAZZ_AMMO_46_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/46.png",
	DisplayName = T(111421465880, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ DisplayName]] "5,7 мм, S109"),
	DisplayNamePlural = T(171557918481, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ DisplayNamePlural]] "5,7 мм, S109"),
	colorStyle = "AmmoBasicColor",
	Description = T(468404152064, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ Description]] "Боеприпас калибра 5.7мм"),
	AdditionalHint = T(500579793552, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	CategoryPair = "57",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_46",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

