UndefineClass('JAZZ_AMMO_50BMG_Incendiary')
DefineClass.JAZZ_AMMO_50BMG_Incendiary = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_incendiary",
	DisplayName = T(123694025099, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Incendiary DisplayName]] ".50, ЗЖ"),
	DisplayNamePlural = T(441685737224, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Incendiary DisplayNamePlural]] ".50, ЗЖ"),
	colorStyle = "AmmoTracerColor",
	Description = T(676306531266, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Incendiary Description]] "Зажигательный боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(436470927890, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_Incendiary AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>горение</color>"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	Caliber = "JAZZ_Caliber_50BMG",
	Modifications = {},
	AppliedEffects = {
		"Exposed",
		"Burning",
	},
	ammo_type_icon = "UI/Icons/Items/ta_shock.png",
}

