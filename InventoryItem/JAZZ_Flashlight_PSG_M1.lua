UndefineClass('JAZZ_Flashlight_PSG_M1')
DefineClass.JAZZ_Flashlight_PSG_M1 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_light",
	DisplayName = T(990002154, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 DisplayName]] "Flashlight"),
	DisplayNamePlural = T(990002155, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 DisplayNamePlural]] "Flashlight"),
	AdditionalHint = T(990002156, --[[ModItemInventoryItemCompositeDef JAZZ_Flashlight_PSG_M1 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	RestockWeight = 5,
	MaxStock = 1,
	Tier = 5,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Flashlight_PSG_M1",
}
