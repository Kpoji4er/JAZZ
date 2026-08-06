UndefineClass('JAZZ_MagBelt_40_100')
DefineClass("JAZZ_MagBelt_40_100", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/expanded_drum_G36_magazine",
	DisplayName = T(990002214, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 DisplayName]] "Короб"),
	DisplayNamePlural = T(990002215, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 DisplayNamePlural]] "Короб"),
	AdditionalHint = T(990002216, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_40_100 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagBelt_40_100",
})
