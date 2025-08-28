UndefineClass('HeavyArmorChestplate_WeavePadding')
DefineClass.HeavyArmorChestplate_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 14,
	Icon = "UI/Icons/Items/heavy_vest",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(218674625854, "Тяжелый жилет"),
	DisplayNamePlural = T(793170991962, "Тяжелые жилеты"),
	AdditionalHint = T(463039026973, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 7000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	PenetrationClass = 4,
	DamageReduction = 45,
	AdditionalReduction = 70,
	ProtectedBodyParts = set( "Torso" ),
}

