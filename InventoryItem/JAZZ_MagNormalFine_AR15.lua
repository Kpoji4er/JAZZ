UndefineClass('JAZZ_MagNormalFine_AR15')
DefineClass.JAZZ_MagNormalFine_AR15 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_MagNormalFine_AR15",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_MagNormalFine_AR15",
	Icon = "UI/Icons/Upgrades/m16_magazine",
	DisplayName = T(990002586, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_AR15 DisplayName]] "Fine-Tuned Mag"),
	DisplayNamePlural = T(990002587, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_AR15 DisplayNamePlural]] "Fine-Tuned Mag"),
	AdditionalHint = T(990002588, --[[ModItemInventoryItemCompositeDef JAZZ_MagNormalFine_AR15 AdditionalHint]] "Семья магазинов: AR15. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 38,
	CategoryPair = "Magazines",
}

