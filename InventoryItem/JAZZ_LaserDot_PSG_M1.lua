UndefineClass('JAZZ_LaserDot_PSG_M1')
DefineClass.JAZZ_LaserDot_PSG_M1 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_LaserDot_PSG_M1",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_LaserDot_PSG_M1",
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002202, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 DisplayName]] "Red Dot"),
	DisplayNamePlural = T(990002203, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 DisplayNamePlural]] "Red Dot"),
	AdditionalHint = T(990002204, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	Tier = 5,
	MaxStock = 1,
	RestockWeight = 5,
	CategoryPair = "Side",
}

