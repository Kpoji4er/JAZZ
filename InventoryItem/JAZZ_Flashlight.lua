UndefineClass('JAZZ_Flashlight')
DefineClass.JAZZ_Flashlight = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Flashlight",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/side_light",
	DisplayName = T(990002139, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight DisplayName]] "Flashlight"),
	DisplayNamePlural = T(990002140, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight DisplayNamePlural]] "Flashlight"),
	AdditionalHint = T(990002141, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "Side",
}

