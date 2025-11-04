UndefineClass('JazzArmor_TireArmor')
DefineClass.JazzArmor_TireArmor = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 M T1",
	object_class = "Armor",
	ScrapParts = 4,
	Icon = "Mod/e6L4ECj/ArmorIcons/TireArmor.png",
	DisplayName = T(230797424385, --[[ModItemInventoryItemCompositeDef JazzArmor_TireArmor DisplayName]] "Самодельная броня из шин"),
	DisplayNamePlural = T(798177913451, --[[ModItemInventoryItemCompositeDef JazzArmor_TireArmor DisplayNamePlural]] "Самодельная броня из шин"),
	Description = T(247198247081, --[[ModItemInventoryItemCompositeDef JazzArmor_TireArmor Description]] "С любовью вырезанная из старых шин для грузовика  полнотельная броня с рукавами. Не хотелось бы огорчать автора жестокой действительностью касательно способностей его брони.\n"),
	AdditionalHint = T(287567251502, --[[ModItemInventoryItemCompositeDef JazzArmor_TireArmor AdditionalHint]] "Самодельная броня из шин"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Torso" ),
	Coverage = 90,
	ArmorRating = 15,
	MeleeArmorRating = 20,
	ExplosiveArmorRating = 25,
	CamouflagePercent = -10,
	CanHoldPlate = true,
	Weight = 3,
	ArmorResource = 250,
	Repairability = 95,
}

