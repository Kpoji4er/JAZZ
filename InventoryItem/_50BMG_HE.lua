UndefineClass('_50BMG_HE')
DefineClass._50BMG_HE = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(948891990549, --[[ModItemInventoryItemCompositeDef _50BMG_HE DisplayName]] ".50, РАЗР"),
	DisplayNamePlural = T(635565288075, --[[ModItemInventoryItemCompositeDef _50BMG_HE DisplayNamePlural]] ".50, РАЗР"),
	colorStyle = "AmmoHPColor",
	Description = T(114582444127, --[[ModItemInventoryItemCompositeDef _50BMG_HE Description]] "Разрывной боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(132438284195, --[[ModItemInventoryItemCompositeDef _50BMG_HE AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания"),
	Cost = 500,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	MaxStacks = 5000,
	Caliber = "50BMG",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationClass",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_subsonic.png",
}

