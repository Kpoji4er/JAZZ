UndefineClass('JazzArmor_GuardianLight')
DefineClass.JazzArmor_GuardianLight = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 L T3",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianL.png",
	DisplayName = T(575595103386, "Бронежилет Гвардиан, Легкий"),
	DisplayNamePlural = T(625019746805, "Бронежилеты Гвардиан, Легкий"),
	Description = T(585745780339, 'Современный модульный бронежилет фирмы "Guardian", являющейся основным поставщиком Ассоциации. Облегченная вариация с защитой только туловища.'),
	AdditionalHint = T(441787897027, "Модульный бронежилет. Облегченный вариант"),
	Cost = 6500,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 55,
	ArmorRating = 14,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 18,
	CanHoldPlate = true,
	Weight = 2,
	ArmorResource = 240,
	Repairability = 65,
}

