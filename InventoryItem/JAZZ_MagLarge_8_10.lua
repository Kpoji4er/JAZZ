UndefineClass('JAZZ_MagLarge_8_10')
DefineClass.JAZZ_MagLarge_8_10 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002283, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_10 DisplayName]] "Магазин на 10 патрон"),
	DisplayNamePlural = T(990002284, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_10 DisplayNamePlural]] "Магазин на 10 патрон"),
	AdditionalHint = T(990002285, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_8_10 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_8_10",
}
