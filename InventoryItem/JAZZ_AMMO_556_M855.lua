UndefineClass('JAZZ_AMMO_556_M855')
DefineClass.JAZZ_AMMO_556_M855 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "M855 - Хорошего качества / Пробивают 3 класс",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556AP.png",
	DisplayName = T(326742931642, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M855 DisplayName]] "5,56 мм, M855"),
	DisplayNamePlural = T(946968976971, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M855 DisplayNamePlural]] "5,56 мм, M855"),
	colorStyle = "AmmoEPRColor",
	Description = T(758340761081, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M855 Description]] "Современный армейский патрон калибра 5.56x45мм."),
	AdditionalHint = T(667602085088, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_M855 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

