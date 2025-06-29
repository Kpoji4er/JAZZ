UndefineClass('JazzArmor_LeatherArmor')
DefineClass.JazzArmor_LeatherArmor = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 M T1",
	object_class = "Armor",
	ScrapParts = 4,
	Icon = "Mod/e6L4ECj/ArmorIcons/LeatherArmor.png",
	DisplayName = T(215116904754, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherArmor DisplayName]] "Кожаная броня"),
	DisplayNamePlural = T(661158179777, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherArmor DisplayNamePlural]] "Кожаная броня"),
	Description = T(970768508285, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherArmor Description]] "Самодельный кожаный нагрудник. По идее, как самостоятельное средство защиты применяться не должен - его нужно проклепать или навешать металлических пластин."),
	AdditionalHint = T(119076303373, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherArmor AdditionalHint]] "Самодельный плотный кожаный нагрудник."),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 40,
	ArmorRating = 10,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 10,
	CamouflagePercent = -5,
	CanHoldPlate = true,
	Weight = 2,
	ArmorResource = 150,
	Repairability = 95,
}

