UndefineClass('JazzArmor_IBALight')
DefineClass.JazzArmor_IBALight = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/IBALight.png",
	DisplayName = T(740197343981, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight DisplayName]] 'Бронежилет "Interceptor"'),
	DisplayNamePlural = T(619300101686, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight DisplayNamePlural]] 'Бронежилет "Interceptor"'),
	Description = T(575083324235, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight Description]] "Современный американский военный бронежилет. Выполнен по всем стандартам проектирования брони - арамидные пакеты усилены керамическими пластинами."),
	AdditionalHint = T(473329167054, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight AdditionalHint]] "Современный американский бронежилет. Облегченный вариант"),
	Cost = 12000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Medium",
	PenetrationClass = 4,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 10,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 22,
	CamouflagePercent = 5,
	CanHoldPlate = true,
	Weight = 3,
}

