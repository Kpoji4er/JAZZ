UndefineClass('JAZZ_ImprovisedSuppressor')
DefineClass.JAZZ_ImprovisedSuppressor = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_ImprovisedSuppressor",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/oil_filter_suppressor_small",
	DisplayName = T(990002193, --[[ModItemInventoryItemCompositeDef JAZZ_ImprovisedSuppressor DisplayName]] "Масляной фильтр"),
	DisplayNamePlural = T(990002194, --[[ModItemInventoryItemCompositeDef JAZZ_ImprovisedSuppressor DisplayNamePlural]] "Масляной фильтр"),
	AdditionalHint = T(990002195, --[[ModItemInventoryItemCompositeDef JAZZ_ImprovisedSuppressor AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "Muzzle",
}

