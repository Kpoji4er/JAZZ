UndefineClass('JazzArmor_LeatherJacketBlk')
DefineClass.JazzArmor_LeatherJacketBlk = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 L T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/LeatherJacket.png",
	DisplayName = T(444430601611, "Кожаная куртка"),
	DisplayNamePlural = T(736065192992, "Кожаные куртки"),
	Description = T(687329018547, "Плотная кожаная мотоциклетная куртка. Может защитить от пары царапин."),
	AdditionalHint = T(168419531911, "Крепкая кожаная куртка."),
	Cost = 100,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 1,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Torso" ),
	Camouflage = true,
	ArmorRating = 5,
	MeleeArmorRating = 4,
	ExplosiveArmorRating = 5,
	ArmorResource = 60,
	Repairability = 80,
}

