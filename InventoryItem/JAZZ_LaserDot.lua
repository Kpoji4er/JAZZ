UndefineClass('JAZZ_LaserDot')
DefineClass.JAZZ_LaserDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_LaserDot",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_LaserDot",
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002196, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot DisplayName]] "Лазерный целеуказатель"),
	DisplayNamePlural = T(990002197, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot DisplayNamePlural]] "Лазерный целеуказатель"),
	AdditionalHint = T(990002198, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Side",
}

