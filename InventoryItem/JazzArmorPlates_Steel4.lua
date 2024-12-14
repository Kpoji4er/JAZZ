UndefineClass('JazzArmorPlates_Steel4')
DefineClass.JazzArmorPlates_Steel4 = {
	__parents = { "ArmorPlates" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 H",
	object_class = "ArmorPlates",
	ScrapParts = 10,
	Repairable = false,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/ArmorPlates/Steel4.png",
	DisplayName = T(135725488589, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel4 DisplayName]] "Стальная бронеплита 4 класса защиты"),
	DisplayNamePlural = T(127967662143, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel4 DisplayNamePlural]] "Стальная бронеплита 4 класса защиты"),
	Description = T(741313418738, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel4 Description]] "Стальная плита 4 класса защиты. Неплохо защищает от винтовочных и автоматных пуль, что дает наемнику право на ошибку."),
	AdditionalHint = T(146117284173, --[[ModItemInventoryItemCompositeDef JazzArmorPlates_Steel4 AdditionalHint]] "Обеспечивает защиту по 4 классу. Вставляется в бронежилеты."),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	Slot = "ArmorPlate",
	PenetrationClass = 4,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
	CanAppearUsed = false,
	ArmorRating = 12,
	Weight = 4,
}

