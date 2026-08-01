UndefineClass('JAZZ_MagLarge_10_20')
DefineClass.JAZZ_MagLarge_10_20 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002235, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20 DisplayName]] "Магазин на 20 патрон"),
	DisplayNamePlural = T(990002236, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20 DisplayNamePlural]] "Магазин на 20 патрон"),
	AdditionalHint = T(990002237, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_10_20",
}
