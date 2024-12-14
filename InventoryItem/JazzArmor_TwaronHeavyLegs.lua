UndefineClass('JazzArmor_TwaronHeavyLegs')
DefineClass.JazzArmor_TwaronHeavyLegs = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/TwaronLegsH.png",
	DisplayName = T(595503417999, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronHeavyLegs DisplayName]] "Тяжелая броня для ног Тварон"),
	DisplayNamePlural = T(887893041975, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronHeavyLegs DisplayNamePlural]] "Тяжелая броня для ног Тварон"),
	Description = T(588731812215, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronHeavyLegs Description]] "Тяжелая защита ног из тварона, состоит из наберенных щитков и наголенников. Чуть хуже защищает от пули, но чуть лучше от ножа."),
	AdditionalHint = T(131153424600, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronHeavyLegs AdditionalHint]] "Тяжелая броня для ног"),
	Valuable = 1,
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 3,
	CategoryPair = "Heavy",
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 70,
	ArmorRating = 16,
	MeleeArmorRating = 18,
	ExplosiveArmorRating = 20,
	Weight = 4,
}

