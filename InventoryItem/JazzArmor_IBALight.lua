UndefineClass('JazzArmor_IBALight')
DefineClass.JazzArmor_IBALight = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 L T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/IBALight.png",
	DisplayName = T(740197343981, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight DisplayName]] 'Бронежилет "Interceptor"'),
	DisplayNamePlural = T(619300101686, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight DisplayNamePlural]] 'Бронежилет "Interceptor"'),
	Description = T(575083324235, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight Description]] "Современный американский военный бронежилет. Выполнен по всем стандартам проектирования брони - арамидные пакеты усилены керамическими пластинами."),
	AdditionalHint = T(473329167054, --[[ModItemInventoryItemCompositeDef JazzArmor_IBALight AdditionalHint]] "Современный американский бронежилет. Облегченный вариант"),
	Cost = 13000,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 19,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 22,
	CamouflagePercent = 5,
	CanHoldPlate = true,
	Weight = 3,
	ArmorResource = 340,
}

