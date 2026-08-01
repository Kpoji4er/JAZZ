UndefineClass('JAZZ_MagLarge_20_30_FAL')
DefineClass.JAZZ_MagLarge_20_30_FAL = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002544, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_20_30_FAL DisplayName]] "Магазин на 30 патрон"),
	DisplayNamePlural = T(990002545, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_20_30_FAL DisplayNamePlural]] "Магазин на 30 патрон"),
	AdditionalHint = T(990002546, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_20_30_FAL AdditionalHint]] "Семья магазинов: FAL. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_20_30_FAL",
}
