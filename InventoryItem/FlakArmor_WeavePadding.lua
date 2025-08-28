UndefineClass('FlakArmor_WeavePadding')
DefineClass.FlakArmor_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 24,
	Icon = "UI/Icons/Items/flak_armor",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(580434125082, "Противооскол. броня"),
	DisplayNamePlural = T(128586439577, "Противооскол. броня"),
	AdditionalHint = T(450301877671, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
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

