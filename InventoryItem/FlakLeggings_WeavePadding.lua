UndefineClass('FlakLeggings_WeavePadding')
DefineClass.FlakLeggings_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 24,
	Icon = "UI/Icons/Items/flak_leggings",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(567301828854, --[[ModItemInventoryItemCompositeDef FlakLeggings_WeavePadding DisplayName]] "Flak Leggings"),
	DisplayNamePlural = T(579822006608, --[[ModItemInventoryItemCompositeDef FlakLeggings_WeavePadding DisplayNamePlural]] "Flak Leggings"),
	Description = "",
	AdditionalHint = T(933954691097, --[[ModItemInventoryItemCompositeDef FlakLeggings_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 1600,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	Slot = "Legs",
	PenetrationClass = 2,
	DamageReduction = 15,
	AdditionalReduction = 45,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

