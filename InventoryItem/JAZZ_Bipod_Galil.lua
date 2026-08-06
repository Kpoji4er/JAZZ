UndefineClass('JAZZ_Bipod_Galil')
DefineClass.JAZZ_Bipod_Galil = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/ak47_bipod",
	DisplayName = T(990002109, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Galil DisplayName]] "Bipod"),
	DisplayNamePlural = T(990002110, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Galil DisplayNamePlural]] "Bipod"),
	AdditionalHint = T(990002111, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Galil AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Under",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Bipod_Galil",
}
