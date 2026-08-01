UndefineClass('JAZZ_UVDot_Anaconda')
DefineClass.JAZZ_UVDot_Anaconda = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laser",
	DisplayName = T(990002406, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot_Anaconda DisplayName]] "UV Dot"),
	DisplayNamePlural = T(990002407, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot_Anaconda DisplayNamePlural]] "UV Dot"),
	AdditionalHint = T(990002408, --[[ModItemInventoryItemCompositeDef JAZZ_UVDot_Anaconda AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_UVDot_Anaconda",
}
