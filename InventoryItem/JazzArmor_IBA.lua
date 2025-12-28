UndefineClass('JazzArmor_IBA')
DefineClass.JazzArmor_IBA = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/IBA.png",
	DisplayName = T(809929737039, 'Бронежилет "Interceptor", с защитой паха'),
	DisplayNamePlural = T(817417475026, 'Бронежилет "Interceptor", с защитой паха'),
	Description = T(893317316245, "Современный американский военный бронежилет. Выполнен по всем стандартам проектирования брони - арамидные пакеты усилены керамическими пластинами. Имеет воротник для защиты шеи и паховую пластину."),
	AdditionalHint = T(799363687481, "Современный американский бронежилет. Средний вариант"),
	Cost = 15000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 6,
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

