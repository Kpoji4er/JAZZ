UndefineClass('KevlarHelmet_Kompositum')
DefineClass.KevlarHelmet_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "UI/Icons/Items/kevlar_helmet",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(403167708542, "Кевларовый шлем с композитумом"),
	DisplayNamePlural = T(627399279577, "Кевларовые шлемы с композитумом"),
	AdditionalHint = T(606562258998, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	Cost = 1800,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "Medium",
	Slot = "Head",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Head" ),
}

