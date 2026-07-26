UndefineClass('KevlarVest_WeavePadding')
DefineClass.KevlarVest_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/kevlar_armor",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(143391465564, --[[ModItemInventoryItemCompositeDef KevlarVest_WeavePadding DisplayName]] "Kevlar Armor"),
	DisplayNamePlural = T(828774839698, --[[ModItemInventoryItemCompositeDef KevlarVest_WeavePadding DisplayNamePlural]] "Kevlar Armors"),
	AdditionalHint = T(497570218481, --[[ModItemInventoryItemCompositeDef KevlarVest_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 5000,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

