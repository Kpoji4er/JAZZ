UndefineClass('JazzArmorPlates_Steel5')
DefineClass.JazzArmorPlates_Steel5 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class5 H",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Steel5.png",
	DisplayName = T(158297465336, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel5 DisplayName]] "Стальная бронеплита 5 класса защиты"),
	DisplayNamePlural = T(580788476785, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel5 DisplayNamePlural]] "Стальная бронеплита 5 класса защиты"),
	Description = T(975821789305, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel5 Description]] "Стальная плита 5 класса защиты. Очень тяжелая, но может остановить даже пулю из Барретта."),
	AdditionalHint = T(681468324000, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel5 AdditionalHint]] "Обеспечивает защиту по 5 классу. Вставляется в бронежилеты."),
	Cost = 7500,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 15,
	CategoryPair = "Heavy",
	Slot = "ArmorPlate",
	PenetrationClass = 4,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 20,
	Weight = 5,
}

