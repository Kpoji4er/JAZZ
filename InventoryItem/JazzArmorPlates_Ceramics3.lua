UndefineClass('JazzArmorPlates_Ceramics3')
DefineClass.JazzArmorPlates_Ceramics3 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 L",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 100,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Ceramics3.png",
	DisplayName = T(732289974638, "Керамическая плита 3 класса защиты"),
	DisplayNamePlural = T(566759096434, "Керамическая плита 3 класса защиты"),
	Description = T(679233924596, "Керамическая пластина 3 класса защиты. Керамические пластины менее долговечные, чем стальные, но лучше защищают"),
	AdditionalHint = T(461117462973, "Обеспечивает защиту по 3 классу. Вставляется в бронежилеты."),
	Cost = 3000,
	CanAppearInShop = true,
	RestockWeight = 20,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 3,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 14,
	Weight = 3,
	ArmorResource = 80,
}

