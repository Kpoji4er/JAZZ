UndefineClass('JAZZ_MagQuick_G36')
DefineClass.JAZZ_MagQuick_G36 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002610, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_G36 DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002611, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_G36 DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002612, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_G36 AdditionalHint]] "Семья магазинов: G36. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_G36",
}
