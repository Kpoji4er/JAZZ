UndefineClass('_44CAL_AP')
DefineClass._44CAL_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(623029149040, --[[ModItemInventoryItemCompositeDef _44CAL_AP DisplayName]] ".44, ББ Отключено"),
	DisplayNamePlural = T(378365287164, --[[ModItemInventoryItemCompositeDef _44CAL_AP DisplayNamePlural]] ".44, ББ Отключено"),
	colorStyle = "AmmoAPColor",
	Description = T(972668654790, --[[ModItemInventoryItemCompositeDef _44CAL_AP Description]] "Бронебойный боеприпас для револьверов и винтовок калибра .44."),
	AdditionalHint = T(501965695809, --[[ModItemInventoryItemCompositeDef _44CAL_AP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность"),
	Cost = 120,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 500,
	Caliber = "",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

