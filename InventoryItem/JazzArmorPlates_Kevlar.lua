UndefineClass('JazzArmorPlates_Kevlar')
DefineClass.JazzArmorPlates_Kevlar = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Kevlar.png",
	DisplayName = T(640356443681, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Kevlar DisplayName]] "Кевларовая бронеплита"),
	DisplayNamePlural = T(633177912309, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Kevlar DisplayNamePlural]] "Кевларовая бронеплита"),
	Description = T(234503579733, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Kevlar Description]] "Легкая кевларовая бронепластина 2 класса защиты. Может неплохо дополнить штатные защитные элементы бронежилета."),
	AdditionalHint = T(310419617432, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Kevlar AdditionalHint]] "Обеспечивает защиту по 2 классу. Вставляется в бронежилеты."),
	Cost = 3000,
	CanAppearInShop = true,
	RestockWeight = 20,
	CategoryPair = "Light",
	Slot = "ArmorPlate",
	PenetrationClass = 2,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 10,
	Weight = 2,
}

