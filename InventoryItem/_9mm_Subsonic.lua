UndefineClass('_9mm_Subsonic')
DefineClass._9mm_Subsonic = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(158230824132, --[[ModItemInventoryItemCompositeDef _9mm_Subsonic DisplayName]] "9mmSubsonicОТКЛЮЧЕНО"),
	DisplayNamePlural = T(307842862228, --[[ModItemInventoryItemCompositeDef _9mm_Subsonic DisplayNamePlural]] "9mmSubsonicОТКЛЮЧЕНО"),
	colorStyle = "AmmoMatchColor",
	Description = T(571319448676, --[[ModItemInventoryItemCompositeDef _9mm_Subsonic Description]] "9 mm ammo for Handguns and SMGs."),
	AdditionalHint = T(404985734712, --[[ModItemInventoryItemCompositeDef _9mm_Subsonic AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Издает меньше шума"),
	Cost = 45,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 500,
	Caliber = "9mm",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "Damage",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_subsonic.png",
}

