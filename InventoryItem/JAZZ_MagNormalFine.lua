UndefineClass('JAZZ_MagNormalFine')
DefineClass.JAZZ_MagNormalFine = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/AK74_Bakelite_magazine",
	DisplayName = T(990002286, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine DisplayName]] "Fine-Tuned Mag"),
	DisplayNamePlural = T(990002287, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine DisplayNamePlural]] "Fine-Tuned Mag"),
	AdditionalHint = T(990002288, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagNormalFine",
}
