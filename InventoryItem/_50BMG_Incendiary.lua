UndefineClass('_50BMG_Incendiary')
DefineClass._50BMG_Incendiary = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(194196164000, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary DisplayName]] ".50, ЗЖ"),
	DisplayNamePlural = T(223133671389, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary DisplayNamePlural]] ".50, ЗЖ"),
	colorStyle = "AmmoTracerColor",
	Description = T(881228785592, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary Description]] "Зажигательный боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(478819781584, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>горение</color>"),
	Cost = 500,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	MaxStacks = 5000,
	Caliber = "50BMG",
	Modifications = {},
	AppliedEffects = {
		"Exposed",
		"Burning",
	},
	ammo_type_icon = "UI/Icons/Items/ta_shock.png",
}

