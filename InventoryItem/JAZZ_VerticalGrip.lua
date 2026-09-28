UndefineClass('JAZZ_VerticalGrip')
DefineClass.JAZZ_VerticalGrip = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_VerticalGrip",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002415, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002416, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002417, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Under",
}

