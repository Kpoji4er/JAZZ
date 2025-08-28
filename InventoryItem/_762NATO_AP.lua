UndefineClass('_762NATO_AP')
DefineClass._762NATO_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "M61 - Бронебойные",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(800158478692, "7.62х51мм НАТО, M61"),
	DisplayNamePlural = T(702196262254, "7.62х51мм НАТО, M61"),
	colorStyle = "AmmoAPColor",
	Description = T(169754239254, "Бронебойный армейский патрон М61 калибра 7.62х51мм НАТО"),
	AdditionalHint = T(538716182691, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 4-м классом брони"),
	Cost = 200,
	Tier = 3,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762NATO",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

