UndefineClass('JazzArmorPlates_Titan3')
DefineClass.JazzArmorPlates_Titan3 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 M",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 85,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Titan3.png",
	DisplayName = T(105991333175, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Titan3 DisplayName]] "Титановая плита 3 класса защиты"),
	DisplayNamePlural = T(539611187321, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Titan3 DisplayNamePlural]] "Титановая плита 3 класса защиты"),
	Description = T(861971172551, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Titan3 Description]] "Титановая бронеплита 3 класса защиты. По пулестойкости титан крепче стали, и гораздо легче нее. Есть и минусы. Цена. И заброневое осколочное действие титана. Но в первую очередь цена, да."),
	AdditionalHint = T(117421137389, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Titan3 AdditionalHint]] "Обеспечивает защиту по 3 классу. Вставляется в бронежилеты."),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 5,
	CategoryPair = "Light",
	Slot = "ArmorPlate",
	PenetrationClass = 3,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 12,
	Weight = 2,
}

