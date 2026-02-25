UndefineClass('JazzArmorPlates_Ceramics5')
DefineClass.JazzArmorPlates_Ceramics5 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class5 L",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 100,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Ceramics5.png",
	DisplayName = T(925634125026, "Керамическая плита 5 класса защиты"),
	DisplayNamePlural = T(932882134462, "Керамическая плита 5 класса защиты"),
	Description = T(538755371034, "Керамическая пластина 5 класса защиты. Очень крепкая. Керамические пластины менее долговечные, чем стальные, но лучше защищают."),
	AdditionalHint = T(626593971199, "Обеспечивает защиту по 5 классу. Вставляется в бронежилеты."),
	Cost = 8000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 10,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 5,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 30,
	Weight = 3,
	ArmorResource = 80,
}

