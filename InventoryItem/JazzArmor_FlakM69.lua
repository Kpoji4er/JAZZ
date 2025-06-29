UndefineClass('JazzArmor_FlakM69')
DefineClass.JazzArmor_FlakM69 = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 N T2",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/FlakM69.png",
	DisplayName = T(385127515445, --[[ModItemInventoryItemCompositeDef JazzArmor_FlakM69 DisplayName]] "Бронежилет Flak M69"),
	DisplayNamePlural = T(306986696662, --[[ModItemInventoryItemCompositeDef JazzArmor_FlakM69 DisplayNamePlural]] "Бронежилеты Flak M69"),
	Description = T(470548861016, --[[ModItemInventoryItemCompositeDef JazzArmor_FlakM69 Description]] 'Модернизированная версия бронежилета "Флак". Фиберглассовые пластины заменены на нейлоновые, что улучшило подвижность бойца. Заодно был добавлен воротник для защиты шеи.'),
	AdditionalHint = T(830324932882, --[[ModItemInventoryItemCompositeDef JazzArmor_FlakM69 AdditionalHint]] "Старый американский бронежилет времен войны во вьетнаме"),
	Cost = 1250,
	CanAppearInShop = true,
	RestockWeight = 15,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 18,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 15,
	CamouflagePercent = 3,
	Weight = 2,
	ArmorResource = 180,
	Repairability = 65,
}

