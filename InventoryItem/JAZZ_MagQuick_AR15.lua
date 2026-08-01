UndefineClass('JAZZ_MagQuick_AR15')
DefineClass.JAZZ_MagQuick_AR15 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002604, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AR15 DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002605, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AR15 DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002606, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AR15 AdditionalHint]] "Семья магазинов: AR15. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_AR15",
}
