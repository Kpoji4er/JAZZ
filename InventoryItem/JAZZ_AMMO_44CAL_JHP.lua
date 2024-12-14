UndefineClass('JAZZ_AMMO_44CAL_JHP')
DefineClass.JAZZ_AMMO_44CAL_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44JHP.png",
	DisplayName = T(385574320141, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP DisplayName]] ".44, JHP"),
	DisplayNamePlural = T(560329197004, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP DisplayNamePlural]] ".44, JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(655933065301, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP Description]] "Экспансивный патрон для револьверов и винтовок калибра .44."),
	AdditionalHint = T(843266944810, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_JHP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 200,
	CanAppearInShop = true,
	MaxStock = 25,
	RestockWeight = 25,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_44CAL",
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
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

