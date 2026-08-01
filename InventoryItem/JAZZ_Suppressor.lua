UndefineClass('JAZZ_Suppressor')
DefineClass.JAZZ_Suppressor = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/deserteagle_suppressor",
	DisplayName = T(990002382, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor DisplayName]] "Suppressor"),
	DisplayNamePlural = T(990002383, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor DisplayNamePlural]] "Suppressor"),
	AdditionalHint = T(990002384, --[[ModItemInventoryItemCompositeDef JAZZ_Suppressor AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Suppressor",
}
