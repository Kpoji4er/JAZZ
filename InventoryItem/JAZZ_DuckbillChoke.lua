UndefineClass('JAZZ_DuckbillChoke')
DefineClass.JAZZ_DuckbillChoke = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/duckbill_choke",
	DisplayName = T(990002133, --[[ModItemInventoryItemCompositeDef JAZZ_DuckbillChoke DisplayName]] "Duckbill Choke"),
	DisplayNamePlural = T(990002134, --[[ModItemInventoryItemCompositeDef JAZZ_DuckbillChoke DisplayNamePlural]] "Duckbill Choke"),
	AdditionalHint = T(990002135, --[[ModItemInventoryItemCompositeDef JAZZ_DuckbillChoke AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_DuckbillChoke",
}
