UndefineClass('JazzArmor_EOD')
DefineClass.JazzArmor_EOD = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 N T2 !!!",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/EOD.png",
	DisplayName = T(385127515445, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayName]] "Бронежилет Flak M69"),
	DisplayNamePlural = T(306986696662, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayNamePlural]] "Бронежилеты Flak M69"),
	Description = T(470548861016, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD Description]] 'Модернизированная версия бронежилета "Флак". Фиберглассовые пластины заменены на нейлоновые, что улучшило подвижность бойца. Заодно был добавлен воротник для защиты шеи.'),
	AdditionalHint = T(830324932882, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD AdditionalHint]] "Старый американский бронежилет времен войны во вьетнаме"),
	Cost = 8500,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 55,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 15,
	MeleeArmorRating = 50,
	ExplosiveArmorRating = 100,
	CamouflagePercent = 3,
	Weight = 5,
	ArmorResource = 180,
	Repairability = 65,
}

