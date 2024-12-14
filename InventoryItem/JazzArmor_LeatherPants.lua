UndefineClass('JazzArmor_LeatherPants')
DefineClass.JazzArmor_LeatherPants = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 N",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 25,
	Icon = "Mod/e6L4ECj/ArmorIcons/LeatherPants.png",
	DisplayName = T(248751035043, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherPants DisplayName]] "Плотные кожаные штаны"),
	DisplayNamePlural = T(681586332311, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherPants DisplayNamePlural]] "Плотные кожаные штаны"),
	Description = T(226438256959, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherPants Description]] "Кожаные штаны. Не только красиво облегают вашу подтянутую задницу, но еще и способны защитить ее от удара ножом."),
	AdditionalHint = T(304254678040, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherPants AdditionalHint]] "Плотные кожаные штаны"),
	Valuable = 1,
	Cost = 300,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 3,
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
	ArmorRating = 10,
	MeleeArmorRating = 7,
}

