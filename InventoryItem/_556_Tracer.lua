UndefineClass('_556_Tracer')
DefineClass._556_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как M855 но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(898687365396, --[[ModItemInventoryItemCompositeDef _556_Tracer DisplayName]] "5,56 мм, M856"),
	DisplayNamePlural = T(553139130283, --[[ModItemInventoryItemCompositeDef _556_Tracer DisplayNamePlural]] "5,56 мм, M856"),
	colorStyle = "AmmoTracerColor",
	Description = T(355232357502, --[[ModItemInventoryItemCompositeDef _556_Tracer Description]] "Современный армейский трассирующий патрон калибра 5.56x45мм."),
	AdditionalHint = T(580519712367, --[[ModItemInventoryItemCompositeDef _556_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ"),
	Cost = 500,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 90,
	Caliber = "556",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

