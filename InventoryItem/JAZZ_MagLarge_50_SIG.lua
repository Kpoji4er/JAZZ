UndefineClass('JAZZ_MagLarge_50_SIG')
DefineClass.JAZZ_MagLarge_50_SIG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002574, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_SIG DisplayName]] "Расширенный магазин"),
	DisplayNamePlural = T(990002575, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_SIG DisplayNamePlural]] "Расширенный магазин"),
	AdditionalHint = T(990002576, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_SIG AdditionalHint]] "Семья магазинов: SIG. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_50_SIG",
}
