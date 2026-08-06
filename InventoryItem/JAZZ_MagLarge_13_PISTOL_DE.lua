UndefineClass('JAZZ_MagLarge_13_PISTOL_DE')
DefineClass.JAZZ_MagLarge_13_PISTOL_DE = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002541, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_13_PISTOL_DE DisplayName]] "Расширенный магазин"),
	DisplayNamePlural = T(990002542, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_13_PISTOL_DE DisplayNamePlural]] "Расширенный магазин"),
	AdditionalHint = T(990002543, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_13_PISTOL_DE AdditionalHint]] "Семья магазинов: PISTOL_DE. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_13_PISTOL_DE",
}
