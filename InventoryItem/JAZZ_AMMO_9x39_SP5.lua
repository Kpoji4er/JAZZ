UndefineClass('JAZZ_AMMO_9x39_SP5')
DefineClass.JAZZ_AMMO_9x39_SP5 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП5",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939SP5.png",
	DisplayName = T(333998606847, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP5 DisplayName]] "9x39 мм, обычный"),
	DisplayNamePlural = T(542771498470, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP5 DisplayNamePlural]] "9x39 мм, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(339244329275, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP5 Description]] "Советский специальный боеприпас СП5 калибра 9х39мм"),
	AdditionalHint = T(265476183448, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP5 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 20,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
}

