UndefineClass('LightHelmet_WeavePadding')
DefineClass.LightHelmet_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 24,
	Icon = "UI/Icons/Items/light_helmet",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(596025389397, --[[ModItemInventoryItemCompositeDef LightHelmet_WeavePadding DisplayName]] "Light Helmet"),
	DisplayNamePlural = T(625172011883, --[[ModItemInventoryItemCompositeDef LightHelmet_WeavePadding DisplayNamePlural]] "Light Helmets"),
	AdditionalHint = T(985499968545, --[[ModItemInventoryItemCompositeDef LightHelmet_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 2000,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	Slot = "Head",
	PenetrationClass = 2,
	DamageReduction = 15,
	AdditionalReduction = 45,
	ProtectedBodyParts = set( "Head" ),
}

