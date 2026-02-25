UndefineClass('JazzArmorPlates_Titan5')
DefineClass.JazzArmorPlates_Titan5 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class5 M",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 85,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Titan5.png",
	DisplayName = T(759722972102, "Титановая плита 5 класса защиты"),
	DisplayNamePlural = T(233593625538, "Титановая плита 5 класса защиты"),
	Description = T(874740516127, "Титановая бронеплита 5 класса защиты. По пулестойкости титан крепче стали, и гораздо легче нее. Есть и минусы. Цена. И заброневое осколочное действие титана. Но в первую очередь цена, да."),
	AdditionalHint = T(165053569449, "Обеспечивает защиту по 5 классу. Вставляется в бронежилеты."),
	Cost = 15000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 1,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 5,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 24,
	Weight = 3,
	ArmorResource = 200,
}

