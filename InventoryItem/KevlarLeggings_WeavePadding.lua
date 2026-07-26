UndefineClass('KevlarLeggings_WeavePadding')
DefineClass.KevlarLeggings_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/kevlar_leggings",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(995619097583, --[[ModItemInventoryItemCompositeDef KevlarLeggings_WeavePadding DisplayName]] "Kevlar Leggings"),
	DisplayNamePlural = T(297011337212, --[[ModItemInventoryItemCompositeDef KevlarLeggings_WeavePadding DisplayNamePlural]] "Kevlar Leggings"),
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

