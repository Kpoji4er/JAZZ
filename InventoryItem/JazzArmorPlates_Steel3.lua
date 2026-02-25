UndefineClass('JazzArmorPlates_Steel3')
DefineClass.JazzArmorPlates_Steel3 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Steel3.png",
	DisplayName = T(237424838471, "Стальная бронеплита 3 класса защиты"),
	DisplayNamePlural = T(125878422803, "Стальная бронеплита 3 класса защиты"),
	Description = T(494083353986, "Стальная плита 3 класса защиты. База."),
	AdditionalHint = T(980856513256, "Обеспечивает защиту по 3 классу. Вставляется в бронежилеты."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 40,
	CategoryPair = "Medium",
	Slot = "ArmorPlate",
	PenetrationClass = 3,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 10,
	Weight = 3,
	ArmorResource = 150,
}

