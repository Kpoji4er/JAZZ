UndefineClass('JazzArmor_UniformCap')
DefineClass.JazzArmor_UniformCap = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class 1 N",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/UniformCap.png",
	DisplayName = T(272785628894, "Военная кепка"),
	DisplayNamePlural = T(777072414296, "Военная кепка"),
	Description = T(336261508886, 'Обычная армейская кепка с козырьком для защиты от яркого солнца. Для услаждения взора командования имеет камуфляжную раскраску "лес"'),
	AdditionalHint = T(188362278685, "Камуфляжная кепка"),
	Valuable = 1,
	Cost = 250,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 10,
	Slot = "Head",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
	ArmorRating = 3,
	CamouflagePercent = 5,
	Vision = 5,
	ArmorResource = 30,
}

