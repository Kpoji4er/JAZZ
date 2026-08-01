UndefineClass('JAZZ_MagLarge_8_BARRET')
DefineClass.JAZZ_MagLarge_8_BARRET = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002577, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_BARRET DisplayName]] "Расширенный магазин"),
	DisplayNamePlural = T(990002578, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_BARRET DisplayNamePlural]] "Расширенный магазин"),
	AdditionalHint = T(990002579, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_BARRET AdditionalHint]] "Семья магазинов: BARRET. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_8_BARRET",
}
