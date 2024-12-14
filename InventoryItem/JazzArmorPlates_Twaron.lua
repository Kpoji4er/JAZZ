UndefineClass('JazzArmorPlates_Twaron')
DefineClass.JazzArmorPlates_Twaron = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 60,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Twaron.png",
	DisplayName = T(527424534974, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Twaron DisplayName]] "Твароновая бронеплита"),
	DisplayNamePlural = T(592682814602, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Twaron DisplayNamePlural]] "Твароновая бронеплита"),
	Description = T(349833670705, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Twaron Description]] "Легкая твароновая бронепластина 2 класса защиты. В дополнение к увеличению защиты от пуль и осколков, также может неплохо остановить лезвие топора какого-нибудь легионовца на спидах."),
	AdditionalHint = T(575439199950, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Twaron AdditionalHint]] "Обеспечивает защиту по 2 классу. Вставляется в бронежилеты."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 20,
	CategoryPair = "Light",
	Slot = "ArmorPlate",
	PenetrationClass = 2,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 8,
	MeleeArmorRating = 10,
	Weight = 2,
	BlockedEffects = {},
}

