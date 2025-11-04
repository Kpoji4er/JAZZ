UndefineClass('LightHelmet_Kompositum')
DefineClass.LightHelmet_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 16,
	Icon = "UI/Icons/Items/light_helmet",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(888518990329, "Легкий шлем с композитумом"),
	DisplayNamePlural = T(552802463500, "Легкие шлемы с композитумом"),
	AdditionalHint = T(309904103984, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Head",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
}

