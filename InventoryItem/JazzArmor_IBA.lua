UndefineClass('JazzArmor_IBA')
DefineClass.JazzArmor_IBA = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/IBA.png",
	DisplayName = T(809929737039, --[[ModItemInventoryItemCompositeDef JazzArmor_IBA DisplayName]] 'Бронежилет "Interceptor", с защитой паха'),
	DisplayNamePlural = T(817417475026, --[[ModItemInventoryItemCompositeDef JazzArmor_IBA DisplayNamePlural]] 'Бронежилет "Interceptor", с защитой паха'),
	Description = T(893317316245, --[[ModItemInventoryItemCompositeDef JazzArmor_IBA Description]] "Современный американский военный бронежилет. Выполнен по всем стандартам проектирования брони - арамидные пакеты усилены керамическими пластинами. Имеет воротник для защиты шеи и паховую пластину."),
	AdditionalHint = T(799363687481, --[[ModItemInventoryItemCompositeDef JazzArmor_IBA AdditionalHint]] "Современный американский бронежилет. Средний вариант"),
	Cost = 16000,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Neck", "Torso" ),
	Coverage = 75,
	ArmorRating = 22,
	MeleeArmorRating = 7,
	ExplosiveArmorRating = 32,
	CamouflagePercent = 5,
	CanHoldPlate = true,
	Weight = 3,
	ArmorResource = 340,
}

