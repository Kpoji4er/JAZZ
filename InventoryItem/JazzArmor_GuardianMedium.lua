UndefineClass('JazzArmor_GuardianMedium')
DefineClass.JazzArmor_GuardianMedium = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianM.png",
	DisplayName = T(491570137761, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianMedium DisplayName]] "Бронежилет Гвардиан, Средний"),
	DisplayNamePlural = T(401793177717, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianMedium DisplayNamePlural]] "Бронежилеты Гвардиан, Средний"),
	Description = T(264423323990, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianMedium Description]] 'Современный модульный бронежилет фирмы "Guardian", являющейся основным поставщиком Ассоциации. Усиленная вариация с защитой паха и воротником.'),
	AdditionalHint = T(288384564314, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianMedium AdditionalHint]] "Модульный бронежилет. Средний вариант"),
	Cost = 8000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 2,
	RestockWeight = 20,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Neck", "Torso" ),
	Coverage = 65,
	ArmorRating = 18,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 22,
	CanHoldPlate = true,
	Weight = 3,
	ArmorResource = 240,
	Repairability = 65,
}

