UndefineClass('_762NATO_Basic')
DefineClass._762NATO_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "М80 - Армейские.",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(208175619329, --[[ModItemInventoryItemCompositeDef _762NATO_Basic DisplayName]] "7.62х51мм НАТО, M80"),
	DisplayNamePlural = T(723121121036, --[[ModItemInventoryItemCompositeDef _762NATO_Basic DisplayNamePlural]] "7.62х51мм НАТО, M80"),
	colorStyle = "BadgeName",
	Description = T(199796874027, --[[ModItemInventoryItemCompositeDef _762NATO_Basic Description]] "Стандартный армейский патрон М80 калибра 7.62х51мм НАТО"),
	AdditionalHint = T(534613659304, --[[ModItemInventoryItemCompositeDef _762NATO_Basic AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 100,
	Tier = 2,
	MaxStock = 30,
	RestockWeight = 50,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762NATO",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

