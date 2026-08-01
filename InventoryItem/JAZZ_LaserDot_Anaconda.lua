UndefineClass('JAZZ_LaserDot_Anaconda')
DefineClass.JAZZ_LaserDot_Anaconda = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002199, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_Anaconda DisplayName]] "Red Dot"),
	DisplayNamePlural = T(990002200, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_Anaconda DisplayNamePlural]] "Red Dot"),
	AdditionalHint = T(990002201, --[[ModItemInventoryItemCompositeDef JAZZ_LaserDot_Anaconda AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_LaserDot_Anaconda",
}
