UndefineClass('JazzArmor_GuardianHelm')
DefineClass.JazzArmor_GuardianHelm = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 M",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianHelm.png",
	DisplayName = T(150785286851, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelm DisplayName]] "Шлем Гвардиан"),
	DisplayNamePlural = T(672638081967, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelm DisplayNamePlural]] "Шлемы Гвардиан"),
	Description = T(119339798394, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelm Description]] 'Несколько лет назад вышедшая на рынок фирма "Guardian" стала основным поставщиком элементов бронезащиты для Ассоциации. Используемые технологии являются коммерческой тайной, но эффективность проводимых Ассоциацией операций в странах третьего мира может многое сказать о качестве их бронежилетов и шлемов.'),
	AdditionalHint = T(856701749869, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHelm AdditionalHint]] "Модульный шлем"),
	Valuable = 1,
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 15,
	CategoryPair = "Medium",
	Slot = "Head",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 70,
	ArmorRating = 25,
	Weight = 3,
	StunGrenadeProtection = 10,
}

