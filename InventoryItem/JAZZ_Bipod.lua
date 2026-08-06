UndefineClass('JAZZ_Bipod')
DefineClass.JAZZ_Bipod = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/Harris_bipod",
	DisplayName = T(990002106, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod DisplayName]] "Bipod"),
	DisplayNamePlural = T(990002107, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod DisplayNamePlural]] "Bipod"),
	AdditionalHint = T(990002108, --[[ModItemInventoryItemCompositeDef JAZZ_Bipod AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Bipod",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Bipod",
}
