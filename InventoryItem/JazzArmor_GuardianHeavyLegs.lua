UndefineClass('JazzArmor_GuardianHeavyLegs')
DefineClass.JazzArmor_GuardianHeavyLegs = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/GuardianLegsH.png",
	DisplayName = T(183467107600, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHeavyLegs DisplayName]] "Тяжелая броня для ног Гвардиан"),
	DisplayNamePlural = T(978936326548, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHeavyLegs DisplayNamePlural]] "Тяжелая броня для ног Гвардиан"),
	Description = T(306694231558, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHeavyLegs Description]] 'Тяжелая защита для ног производства фирмы "Guardian". Хорошее соотношение веса и защищенности, защищает бедра и голени на всем протяжении.'),
	AdditionalHint = T(313703635746, --[[ModItemInventoryItemCompositeDef JazzArmor_GuardianHeavyLegs AdditionalHint]] "Тяжелая броня для ног"),
	Valuable = 1,
	Cost = 10000,
	CanAppearInShop = true,
	RestockWeight = 3,
	CategoryPair = "Heavy",
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 70,
	ArmorRating = 16,
	MeleeArmorRating = 15,
	ExplosiveArmorRating = 15,
	Weight = 4,
	SuppressionProtection = 15,
}

