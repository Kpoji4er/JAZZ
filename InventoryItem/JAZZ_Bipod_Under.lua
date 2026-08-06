UndefineClass('JAZZ_Bipod_Under')
DefineClass.JAZZ_Bipod_Under = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/ak47_bipod",
	DisplayName = T(990002112, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Under DisplayName]] "Bipod"),
	DisplayNamePlural = T(990002113, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Under DisplayNamePlural]] "Bipod"),
	AdditionalHint = T(990002114, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod_Under AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Under",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Bipod_Under",
}
