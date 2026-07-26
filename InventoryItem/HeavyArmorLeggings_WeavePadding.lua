UndefineClass('HeavyArmorLeggings_WeavePadding')
DefineClass.HeavyArmorLeggings_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 14,
	Icon = "UI/Icons/Items/heavy_leggings",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(900851966356, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings_WeavePadding DisplayName]] "Heavy Armor Leggings"),
	DisplayNamePlural = T(383152125619, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings_WeavePadding DisplayNamePlural]] "Heavy Armor Leggings"),
	AdditionalHint = T(667037980727, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 7000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	Slot = "Legs",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

