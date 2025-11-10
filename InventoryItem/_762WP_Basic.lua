UndefineClass('_762WP_Basic')
DefineClass._762WP_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "ПС - Армейские. В основном у бобби рея",
	object_class = "Ammo",
	RepairCost = 400,
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(470221441895, --[[ModItemInventoryItemCompositeDef _762WP_Basic DisplayName]] "7,62х39мм, ПС"),
	DisplayNamePlural = T(428309489295, --[[ModItemInventoryItemCompositeDef _762WP_Basic DisplayNamePlural]] "7,62х39мм, ПС"),
	colorStyle = "BadgeName",
	Description = T(393515769284, --[[ModItemInventoryItemCompositeDef _762WP_Basic Description]] "Стандартный советский армейский патрон ПС калибра 7.62х39мм"),
	AdditionalHint = T(613363959995, --[[ModItemInventoryItemCompositeDef _762WP_Basic AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 300,
	Tier = 3,
	MaxStock = 10,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762WP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

