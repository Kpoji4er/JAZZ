UndefineClass('HeavyArmorHelmet_Kompositum')
DefineClass.HeavyArmorHelmet_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "UI/Icons/Items/heavy_helmet",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(789934266572, "Тяжелый шлем с композитумом"),
	DisplayNamePlural = T(454707438160, "Тяжелые шлемы с композитумом"),
	AdditionalHint = T(312770121832, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещено с композитумом-58"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 5000,
	Tier = 3,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	Slot = "Head",
	PenetrationClass = 5,
	DamageReduction = 35,
	AdditionalReduction = 85,
	ProtectedBodyParts = set( "Head" ),
}

