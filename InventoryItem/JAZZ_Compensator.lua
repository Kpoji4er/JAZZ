UndefineClass('JAZZ_Compensator')
DefineClass.JAZZ_Compensator = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/MP5_compensator",
	DisplayName = T(990002130, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator DisplayName]] "Compensator"),
	DisplayNamePlural = T(990002131, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator DisplayNamePlural]] "Compensator"),
	AdditionalHint = T(990002132, --[[ModItemInventoryItemCompositeDef JAZZ_Compensator AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Compensator",
}
