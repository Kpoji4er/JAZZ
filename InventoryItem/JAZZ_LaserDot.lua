UndefineClass('JAZZ_LaserDot')
DefineClass.JAZZ_LaserDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002196, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot DisplayName]] "Лазерный целеуказатель"),
	DisplayNamePlural = T(990002197, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot DisplayNamePlural]] "Лазерный целеуказатель"),
	AdditionalHint = T(990002198, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 28,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_LaserDot",
}
