UndefineClass('JazzArmorPlates_Titan4')
DefineClass.JazzArmorPlates_Titan4 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 M",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 85,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Titan4.png",
	DisplayName = T(810499546011, "Титановая плита 4 класса защиты"),
	DisplayNamePlural = T(796049810331, "Титановая плита 4 класса защиты"),
	Description = T(295853758396, "Титановая бронеплита 4 класса защиты. По пулестойкости титан крепче стали, и гораздо легче нее. Есть и минусы. Цена. И заброневое осколочное действие титана. Но в первую очередь цена, да."),
	AdditionalHint = T(694193912756, "Обеспечивает защиту по 4 классу. Вставляется в бронежилеты."),
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 3,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 4,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 16,
	Weight = 3,
	ArmorResource = 200,
}

