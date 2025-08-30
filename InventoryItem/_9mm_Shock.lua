UndefineClass('_9mm_Shock')
DefineClass._9mm_Shock = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(560400460237, --[[ModItemInventoryItemCompositeDef _9mm_Shock DisplayName]] "9mm ShockОТКЛЮЧЕНО"),
	DisplayNamePlural = T(733411942262, --[[ModItemInventoryItemCompositeDef _9mm_Shock DisplayNamePlural]] "9mm ShockОТКЛЮЧЕНО"),
	colorStyle = "AmmoMatchColor",
	Description = T(330508860958, --[[ModItemInventoryItemCompositeDef _9mm_Shock Description]] "Шоковый боеприпас для пистолетов, револьверов и пистолетов-пулеметов калибра 9 мм."),
	AdditionalHint = T(595335142998, --[[ModItemInventoryItemCompositeDef _9mm_Shock AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сниженная дальнобойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 90,
	Tier = 2,
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
	AppliedEffects = {
		"Exposed",
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_shock.png",
}

