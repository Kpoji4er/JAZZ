UndefineClass('JAZZ_MagNormalFine_FAL')
DefineClass.JAZZ_MagNormalFine_FAL = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/m16_magazine",
	DisplayName = T(990002589, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL DisplayName]] "Fine-Tuned Mag"),
	DisplayNamePlural = T(990002590, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL DisplayNamePlural]] "Fine-Tuned Mag"),
	AdditionalHint = T(990002591, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_FAL AdditionalHint]] "Семья магазинов: FAL. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagNormalFine_FAL",
}
