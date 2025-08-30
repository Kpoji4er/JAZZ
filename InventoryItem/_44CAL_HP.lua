UndefineClass('_44CAL_HP')
DefineClass._44CAL_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(382334892926, --[[ModItemInventoryItemCompositeDef _44CAL_HP DisplayName]] ".44, JHP"),
	DisplayNamePlural = T(442558127075, --[[ModItemInventoryItemCompositeDef _44CAL_HP DisplayNamePlural]] ".44, JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(199064256585, --[[ModItemInventoryItemCompositeDef _44CAL_HP Description]] "Экспансивный патрон для револьверов и винтовок калибра .44."),
	AdditionalHint = T(328885827009, --[[ModItemInventoryItemCompositeDef _44CAL_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 200,
	MaxStock = 25,
	RestockWeight = 25,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 1500,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

