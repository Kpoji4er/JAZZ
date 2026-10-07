UndefineClass('JAZZ_UVDot')
DefineClass.JAZZ_UVDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_UVDot",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_UVDot",
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002403, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot DisplayName]] "UV Dot"),
	DisplayNamePlural = T(990002404, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot DisplayNamePlural]] "UV Dot"),
	AdditionalHint = T(990002405, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "Side",
}

