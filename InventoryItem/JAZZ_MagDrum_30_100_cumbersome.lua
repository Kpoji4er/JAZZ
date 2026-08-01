UndefineClass('JAZZ_MagDrum_30_100_cumbersome')
DefineClass("JAZZ_MagDrum_30_100_cumbersome", {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/expanded_drum_G36_magazine",
	DisplayName = T(990002220, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_cumbersome DisplayName]] "Бубен"),
	DisplayNamePlural = T(990002221, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_cumbersome DisplayNamePlural]] "Бубен"),
	AdditionalHint = T(990002222, --[[ModItemInventoryItemCompositeDef JAZZ_MagDrum_30_100_cumbersome AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagDrum_30_100_cumbersome",
})
