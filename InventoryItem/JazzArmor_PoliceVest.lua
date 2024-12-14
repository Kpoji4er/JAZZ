UndefineClass('JazzArmor_PoliceVest')
DefineClass.JazzArmor_PoliceVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 L T3",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/Police.png",
	DisplayName = T(735699102530, --[[ModItemInventoryItemCompositeDef JazzArmor_PoliceVest DisplayName]] "Полицейский бронежилет"),
	DisplayNamePlural = T(338967629493, --[[ModItemInventoryItemCompositeDef JazzArmor_PoliceVest DisplayNamePlural]] "Полицейские бронежилеты"),
	Description = T(225370809188, --[[ModItemInventoryItemCompositeDef JazzArmor_PoliceVest Description]] "Бронежилет, используемый полицейскими структурами чуть не по всему миру. Кевларовая ткань обеспечивает уровень защиты, достаточный против большинства преступников, вооруженных легким оружием и не очень хорошо умеющих стрелять из него."),
	AdditionalHint = T(309353881675, --[[ModItemInventoryItemCompositeDef JazzArmor_PoliceVest AdditionalHint]] "Полицейский бронежилет. Облегченный вариант"),
	Cost = 2500,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 50,
	ArmorRating = 10,
	MeleeArmorRating = 15,
	ExplosiveArmorRating = 12,
	CamouflagePercent = -5,
	CanHoldPlate = true,
	Weight = 2,
}

