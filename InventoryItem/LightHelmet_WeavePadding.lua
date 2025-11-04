UndefineClass('LightHelmet_WeavePadding')
DefineClass.LightHelmet_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 24,
	Icon = "UI/Icons/Items/light_helmet",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(656393644870, "Легкий шлем"),
	DisplayNamePlural = T(867812156182, "Легкие шлемы"),
	AdditionalHint = T(985499968545, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 2000,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	Slot = "Head",
	PenetrationClass = 2,
	DamageReduction = 15,
	AdditionalReduction = 45,
	ProtectedBodyParts = set( "Head" ),
}

