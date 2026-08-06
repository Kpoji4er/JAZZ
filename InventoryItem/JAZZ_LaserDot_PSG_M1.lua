UndefineClass('JAZZ_LaserDot_PSG_M1')
DefineClass.JAZZ_LaserDot_PSG_M1 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002202, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 DisplayName]] "Red Dot"),
	DisplayNamePlural = T(990002203, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 DisplayNamePlural]] "Red Dot"),
	AdditionalHint = T(990002204, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_PSG_M1 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 5,
	MaxStock = 1,
	Tier = 5,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_LaserDot_PSG_M1",
}
