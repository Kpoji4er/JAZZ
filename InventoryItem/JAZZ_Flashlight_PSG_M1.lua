UndefineClass('JAZZ_Flashlight_PSG_M1')
DefineClass.JAZZ_Flashlight_PSG_M1 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Flashlight_PSG_M1",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_Flashlight_PSG_M1",
	Icon = "UI/Icons/Upgrades/side_light",
	DisplayName = T(990002154, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 DisplayName]] "Flashlight"),
	DisplayNamePlural = T(990002155, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 DisplayNamePlural]] "Flashlight"),
	AdditionalHint = T(990002156, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	Tier = 5,
	MaxStock = 1,
	RestockWeight = 5,
	CategoryPair = "Side",
}

