UndefineClass('JAZZ_AMMO_792_FMJ')
DefineClass.JAZZ_AMMO_792_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/792x57.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ DisplayName]] "7,92х57 мм, обычный"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ DisplayNamePlural]] "7,92х57 мм, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ Description]] "Немецкий боеприпас калибра 7.92х57мм Маузер"),
	AdditionalHint = T(727230096414, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 5,
	CategoryPair = "792",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_792",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

