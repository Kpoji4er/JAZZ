UndefineClass('JAZZ_UVDot')
DefineClass.JAZZ_UVDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002403, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot DisplayName]] "UV Dot"),
	DisplayNamePlural = T(990002404, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot DisplayNamePlural]] "UV Dot"),
	AdditionalHint = T(990002405, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 40,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_UVDot",
}
