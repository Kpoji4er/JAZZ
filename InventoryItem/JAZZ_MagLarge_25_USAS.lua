UndefineClass('JAZZ_MagLarge_25_USAS')
DefineClass.JAZZ_MagLarge_25_USAS = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002559, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_25_USAS DisplayName]] "Расширенный магазин"),
	DisplayNamePlural = T(990002560, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_25_USAS DisplayNamePlural]] "Расширенный магазин"),
	AdditionalHint = T(990002561, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_25_USAS AdditionalHint]] "Семья магазинов: USAS. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_25_USAS",
}
