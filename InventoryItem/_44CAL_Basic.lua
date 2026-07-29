UndefineClass('_44CAL_Basic')
DefineClass._44CAL_Basic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(816672875398, --[[ModItemInventoryItemCompositeDef _44CAL_Basic DisplayName]] ".44, FMJ"),
	DisplayNamePlural = T(754359355166, --[[ModItemInventoryItemCompositeDef _44CAL_Basic DisplayNamePlural]] ".44, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(865667887261, --[[ModItemInventoryItemCompositeDef _44CAL_Basic Description]] "Стандартный патрон для револьверов и винтовок калибра .44."),
	AdditionalHint = T(413139999089, --[[ModItemInventoryItemCompositeDef _44CAL_Basic AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 40,
	MaxStock = 50,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 60,
	Caliber = "44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
	},
}

