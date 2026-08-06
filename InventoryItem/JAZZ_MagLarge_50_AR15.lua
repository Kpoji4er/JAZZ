UndefineClass('JAZZ_MagLarge_50_AR15')
DefineClass.JAZZ_MagLarge_50_AR15 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002565, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_AR15 DisplayName]] "Расширенный магазин"),
	DisplayNamePlural = T(990002566, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_AR15 DisplayNamePlural]] "Расширенный магазин"),
	AdditionalHint = T(990002567, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_50_AR15 AdditionalHint]] "Семья магазинов: AR15. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_50_AR15",
}
