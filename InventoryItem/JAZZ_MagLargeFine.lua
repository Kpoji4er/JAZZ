UndefineClass('JAZZ_MagLargeFine')
DefineClass.JAZZ_MagLargeFine = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/expanded_AK47_magazine",
	DisplayName = T(990002232, --[[ModItemInventoryItemCompositeDef JAZZ_MagLargeFine DisplayName]] "Ergonomic Expanded Mag"),
	DisplayNamePlural = T(990002233, --[[ModItemInventoryItemCompositeDef JAZZ_MagLargeFine DisplayNamePlural]] "Ergonomic Expanded Mag"),
	AdditionalHint = T(990002234, --[[ModItemInventoryItemCompositeDef JAZZ_MagLargeFine AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLargeFine",
}
