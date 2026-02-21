UndefineClass('_556_AP')
DefineClass._556_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "M855 - Хорошего качества / Пробивают 3 класс",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(472452415737, --[[ModItemInventoryItemCompositeDef _556_AP DisplayName]] "5,56 мм, M855"),
	DisplayNamePlural = T(529286090617, --[[ModItemInventoryItemCompositeDef _556_AP DisplayNamePlural]] "5,56 мм, M855"),
	colorStyle = "AmmoAPColor",
	Description = T(840673411268, --[[ModItemInventoryItemCompositeDef _556_AP Description]] "Современный армейский патрон калибра 5.56x45мм."),
	AdditionalHint = T(984094647243, --[[ModItemInventoryItemCompositeDef _556_AP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 500,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

