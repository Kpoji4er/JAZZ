UndefineClass('JAZZ_VerticalGrip')
DefineClass.JAZZ_VerticalGrip = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002415, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002416, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002417, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 28,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Under",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_VerticalGrip",
}
