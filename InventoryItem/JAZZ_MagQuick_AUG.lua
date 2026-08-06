UndefineClass('JAZZ_MagQuick_AUG')
DefineClass.JAZZ_MagQuick_AUG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002607, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002608, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002609, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AUG AdditionalHint]] "Семья магазинов: AUG. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_AUG",
}
