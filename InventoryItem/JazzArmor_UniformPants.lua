UndefineClass('JazzArmor_UniformPants')
DefineClass.JazzArmor_UniformPants = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 N",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/UniformPants.png",
	DisplayName = T(418702320610, "Военные штаны"),
	DisplayNamePlural = T(601867100326, "Военные штаны"),
	Description = T(770209843536, "Форменные армейские штаны в камуфляжной расцветке."),
	AdditionalHint = T(755249659005, "Камуфляжные штаны"),
	Valuable = 1,
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 15,
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
	ArmorRating = 6,
	MeleeArmorRating = 2,
	CamouflagePercent = 20,
	ArmorResource = 60,
	Repairability = 80,
}

