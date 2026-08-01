UndefineClass('JAZZ_PistolSuppressor')
DefineClass.JAZZ_PistolSuppressor = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/deserteagle_suppressor",
	DisplayName = T(990002313, --[[ModItemInventoryItemCompositeDef JAZZ_PistolSuppressor DisplayName]] "Глушитель"),
	DisplayNamePlural = T(990002314, --[[ModItemInventoryItemCompositeDef JAZZ_PistolSuppressor DisplayNamePlural]] "Глушитель"),
	AdditionalHint = T(990002315, --[[ModItemInventoryItemCompositeDef JAZZ_PistolSuppressor AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_PistolSuppressor",
}
