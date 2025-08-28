UndefineClass('_762NATO_Basic')
DefineClass._762NATO_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "М80 - Армейские.",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(208175619329, "7.62х51мм НАТО, M80"),
	DisplayNamePlural = T(723121121036, "7.62х51мм НАТО, M80"),
	colorStyle = "AmmoGreenColor",
	Description = T(199796874027, "Стандартный армейский патрон М80 калибра 7.62х51мм НАТО"),
	AdditionalHint = T(534613659304, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
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

