UndefineClass('PostApoHelmet')
DefineClass.PostApoHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	CanAppearInShop = false,
	Cost = 2600,
	ScrapParts = 2,
	Degradation = 60,
	Icon = "UI/Icons/Items/post_apo_helmet",
	DisplayName = T(632051696391, --[[ModItemInventoryItemCompositeDef PostApoHelmet DisplayName]] "Shiny and Chrome Helmet"),
	DisplayNamePlural = T(382736672530, --[[ModItemInventoryItemCompositeDef PostApoHelmet DisplayNamePlural]] "Shiny and Chrome Helmets"),
	AdditionalHint = T(164667458744, --[[ModItemInventoryItemCompositeDef PostApoHelmet AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ломается ОЧЕНЬ часто\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Плюс 100 к безумию"),
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Head",
	PenetrationClass = 4,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
}

