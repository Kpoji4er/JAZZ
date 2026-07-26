UndefineClass('_9mm_Tracer')
DefineClass._9mm_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(572390972773, --[[ModItemInventoryItemCompositeDef _9mm_Tracer DisplayName]] "9mmTracerОТКЛЮЧЕНО"),
	DisplayNamePlural = T(489176470960, --[[ModItemInventoryItemCompositeDef _9mm_Tracer DisplayNamePlural]] "9mmTracerОТКЛЮЧЕНО"),
	colorStyle = "AmmoTracerColor",
	Description = T(605716564475, --[[ModItemInventoryItemCompositeDef _9mm_Tracer Description]] "9 mm ammo for Handguns and SMGs."),
	AdditionalHint = T(647181592030, --[[ModItemInventoryItemCompositeDef _9mm_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 60,
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
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

