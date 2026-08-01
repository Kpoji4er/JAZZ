UndefineClass('JAZZ_MagQuick_GALIL')
DefineClass.JAZZ_MagQuick_GALIL = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002613, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_GALIL DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002614, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_GALIL DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002615, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_GALIL AdditionalHint]] "Семья магазинов: GALIL. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_GALIL",
}
