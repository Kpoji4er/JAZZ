UndefineClass('JazzArmor_Uniform')
DefineClass.JazzArmor_Uniform = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 L T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/Uniform.png",
	DisplayName = T(978505280466, "Военная униформа"),
	DisplayNamePlural = T(272625731444, "Военная униформа"),
	Description = T(589956058960, "Форменная армейская рубашка в камуфляжной расцветке."),
	AdditionalHint = T(340489681757, "Камуфляжная военная форма"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	ArmorRating = 8,
	MeleeArmorRating = 2,
	ExplosiveArmorRating = 20,
	CamouflagePercent = 20,
	Repairability = 80,
}

