UndefineClass('PostApoHelmet')
DefineClass.PostApoHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 60,
	Icon = "UI/Icons/Items/post_apo_helmet",
	DisplayName = T(883936367090, --[[ModItemInventoryItemCompositeDef PostApoHelmet DisplayName]] "Блестящий шлем"),
	DisplayNamePlural = T(343660006188, --[[ModItemInventoryItemCompositeDef PostApoHelmet DisplayNamePlural]] "Блестящие шлемы"),
	AdditionalHint = T(164667458744, --[[ModItemInventoryItemCompositeDef PostApoHelmet AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ломается ОЧЕНЬ часто\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Плюс 100 к безумию"),
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Head",
	PenetrationClass = 4,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
}

