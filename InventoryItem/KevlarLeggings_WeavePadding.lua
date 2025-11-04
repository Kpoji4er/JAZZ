UndefineClass('KevlarLeggings_WeavePadding')
DefineClass.KevlarLeggings_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/kevlar_leggings",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(889185234463, --[[ModItemInventoryItemCompositeDef KevlarLeggings_WeavePadding DisplayName]] "Кевларовые поножи"),
	DisplayNamePlural = T(361740896558, --[[ModItemInventoryItemCompositeDef KevlarLeggings_WeavePadding DisplayNamePlural]] "Кевларовые поножи"),
	AdditionalHint = T(547092855750, --[[ModItemInventoryItemCompositeDef KevlarLeggings_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 2800,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

