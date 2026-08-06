UndefineClass('JazzArmor_SWAT')
DefineClass.JazzArmor_SWAT = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 H T2",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/SWAT.png",
	DisplayName = T(203947535559, --[[ModItemInventoryItemCompositeDef JazzArmor_SWAT DisplayName]] "Бронежилет SWAT"),
	DisplayNamePlural = T(426940580107, --[[ModItemInventoryItemCompositeDef JazzArmor_SWAT DisplayNamePlural]] "Бронежилеты SWAT"),
	Description = T(551876545420, --[[ModItemInventoryItemCompositeDef JazzArmor_SWAT Description]] 'Тяжелый полицейский штурмовой бронежилет с дополнительной защитой паха, шеи и рукавов. Применяется силами специального назначения на особо тяжелых "адресах".'),
	AdditionalHint = T(917398081831, --[[ModItemInventoryItemCompositeDef JazzArmor_SWAT AdditionalHint]] "Полицейский бронежилет. Тяжелый вариант для специальных операций"),
	Cost = 4800,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 80,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Neck", "Torso" ),
	Coverage = 95,
	ArmorRating = 18,
	MeleeArmorRating = 30,
	ExplosiveArmorRating = 30,
	CamouflagePercent = -15,
	CanHoldPlate = true,
	Weight = 4,
	ArmorResource = 250,
}

