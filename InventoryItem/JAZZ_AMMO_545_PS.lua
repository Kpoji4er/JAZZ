UndefineClass('JAZZ_AMMO_545_PS')
DefineClass.JAZZ_AMMO_545_PS = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ПС - Армейские. В основном у бобби рея",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545.png",
	DisplayName = T(827774006254, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PS DisplayName]] "5,45 мм, ПС"),
	DisplayNamePlural = T(138469521759, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PS DisplayNamePlural]] "5,45 мм, ПС"),
	colorStyle = "AmmoGreenColor",
	Description = T(930854241886, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PS Description]] "Стандартный российский армейский патрон 7Н6 калибра 5.45x39мм"),
	AdditionalHint = T(213021415103, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_PS AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 400,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 15,
	RestockWeight = 50,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
}

