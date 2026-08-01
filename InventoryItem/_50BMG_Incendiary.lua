UndefineClass('_50BMG_Incendiary')
DefineClass._50BMG_Incendiary = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(727344246325, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary DisplayName]] ".50 Frag"),
	DisplayNamePlural = T(468293090203, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary DisplayNamePlural]] ".50 Frag"),
	colorStyle = "AmmoTracerColor",
	Description = T(196314399167, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary Description]] ".50 Ammo for Machine Guns, Snipers and Handguns."),
	AdditionalHint = T(478819781584, --[[ModItemInventoryItemCompositeDef _50BMG_Incendiary AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>горение</color>"),
	Cost = 500,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	MaxStacks = 40,
	Caliber = "50BMG",
	Modifications = {},
	AppliedEffects = {
		"ExposedBurning",
	},
	ammo_type_icon = "UI/Icons/Items/ta_shock.png",
}

