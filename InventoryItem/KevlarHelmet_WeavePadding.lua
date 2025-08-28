UndefineClass('KevlarHelmet_WeavePadding')
DefineClass.KevlarHelmet_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 20,
	Icon = "UI/Icons/Items/kevlar_helmet",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(409561352971, "Кевларовый шлем"),
	DisplayNamePlural = T(767764349157, "Кевларовые шлемы"),
	AdditionalHint = T(507191349868, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 3600,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	Slot = "Head",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Head" ),
}

