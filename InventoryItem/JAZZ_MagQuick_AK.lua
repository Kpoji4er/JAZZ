UndefineClass('JAZZ_MagQuick_AK')
DefineClass.JAZZ_MagQuick_AK = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002601, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AK DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002602, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AK DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002603, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_AK AdditionalHint]] "Семья магазинов: AK. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 38,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_AK",
}
