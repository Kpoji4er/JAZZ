UndefineClass('JAZZ_MagBelt_100_200')
DefineClass("JAZZ_MagBelt_100_200", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/expanded_drum_G36_magazine",
	DisplayName = T(990002211, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_100_200 DisplayName]] "Увеличенный короб"),
	DisplayNamePlural = T(990002212, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_100_200 DisplayNamePlural]] "Увеличенный короб"),
	AdditionalHint = T(990002213, --[[ModItemInventoryItemCompositeDef JAZZ_MagBelt_100_200 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 10000,
	CanAppearInShop = true,
	RestockWeight = 5,
	MaxStock = 1,
	Tier = 5,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagBelt_100_200",
})
