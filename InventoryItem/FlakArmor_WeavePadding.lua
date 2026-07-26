UndefineClass('FlakArmor_WeavePadding')
DefineClass.FlakArmor_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 24,
	Icon = "UI/Icons/Items/flak_armor",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(336822464699, --[[ModItemInventoryItemCompositeDef FlakArmor_WeavePadding DisplayName]] "Flak Armor"),
	DisplayNamePlural = T(250499294314, --[[ModItemInventoryItemCompositeDef FlakArmor_WeavePadding DisplayNamePlural]] "Flak Armors"),
	AdditionalHint = T(450301877671, --[[ModItemInventoryItemCompositeDef FlakArmor_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 2400,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	PenetrationClass = 2,
	DamageReduction = 15,
	AdditionalReduction = 45,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

