UndefineClass('JazzArmor_TwaronLegs')
DefineClass.JazzArmor_TwaronLegs = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 M",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/TwaronLegs.png",
	DisplayName = T(340564452388, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronLegs DisplayName]] "Легкая броня для ног Тварон"),
	DisplayNamePlural = T(501827511664, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronLegs DisplayNamePlural]] "Легкая броня для ног Тварон"),
	Description = T(982146278290, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronLegs Description]] "Набедренные щитки из тварона. Чуть хуже защищат от пули, но чуть лучше от ножа."),
	AdditionalHint = T(875990093803, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronLegs AdditionalHint]] "Легкия броня для ног"),
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "Medium",
	Slot = "Legs",
	PenetrationClass = 2,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 50,
	ArmorRating = 14,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 10,
	Weight = 3,
	SuppressionProtection = 5,
}

