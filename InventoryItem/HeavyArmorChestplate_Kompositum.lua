UndefineClass('HeavyArmorChestplate_Kompositum')
DefineClass.HeavyArmorChestplate_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/heavy_vest",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(629905031350, "Тяжелый жилет с композитумом"),
	DisplayNamePlural = T(457665882082, "Тяжелые жилеты с композитумом"),
	AdditionalHint = T(750816289329, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещено с композитумом-58"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 4300,
	Tier = 3,
	RestockWeight = 50,
	CategoryPair = "Heavy",
	PenetrationClass = 5,
	DamageReduction = 40,
	AdditionalReduction = 85,
	ProtectedBodyParts = set( "Torso" ),
}

