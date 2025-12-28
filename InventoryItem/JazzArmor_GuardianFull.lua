UndefineClass('JazzArmor_GuardianFull')
DefineClass.JazzArmor_GuardianFull = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianH.png",
	DisplayName = T(599122251974, "Бронежилет Гвардиан, Тяжелый"),
	DisplayNamePlural = T(782617276071, "Бронежилеты Гвардиан, Тяжелый"),
	Description = T(739427349184, 'Современный модульный бронежилет фирмы "Guardian", являющейся основным поставщиком Ассоциации. Тяжелая штурмовая вариация с защитой корпуса, шеи, паха и рук.'),
	AdditionalHint = T(829471117799, "Модульный бронежилет. Штурмовой вариант"),
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Heavy",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Neck", "Torso" ),
	Coverage = 95,
	ArmorRating = 23,
	MeleeArmorRating = 12,
	ExplosiveArmorRating = 35,
	CanHoldPlate = true,
	Weight = 4,
	ArmorResource = 240,
	Repairability = 65,
}

