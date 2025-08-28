UndefineClass('JazzArmorPlates_Ceramics4')
DefineClass.JazzArmorPlates_Ceramics4 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 L",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 100,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Ceramics4.png",
	DisplayName = T(282059758278, "Керамическая плита 4 класса защиты"),
	DisplayNamePlural = T(447009212548, "Керамическая плита 4 класса защиты"),
	Description = T(326206091502, "Керамическая пластина 4 класса защиты. Керамические пластины менее долговечные, чем стальные, но лучше защищают."),
	AdditionalHint = T(472781199909, "Обеспечивает защиту по 4 классу. Вставляется в бронежилеты."),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 15,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 4,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 20,
	Weight = 3,
	ArmorResource = 80,
}

