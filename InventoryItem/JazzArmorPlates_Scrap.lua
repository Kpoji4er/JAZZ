UndefineClass('JazzArmorPlates_Scrap')
DefineClass.JazzArmorPlates_Scrap = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 90,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Scrap.png",
	DisplayName = T(422095393043, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Scrap DisplayName]] "Самодельная бронеплита"),
	DisplayNamePlural = T(627000349514, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Scrap DisplayNamePlural]] "Самодельная бронеплита"),
	Description = T(618294702085, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Scrap Description]] "Самодельная бронепластина из гнилого ржавого железа. Легион в огромном количестве снабжает своих бойцов такими."),
	AdditionalHint = T(430834060272, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Scrap AdditionalHint]] "Обеспечивает защиту по 1 классу. Вставляется в бронежилеты."),
	Cost = 800,
	CanAppearInShop = false,
	Slot = "ArmorPlate",
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 10,
	Weight = 4,
	ArmorResource = 250,
}

