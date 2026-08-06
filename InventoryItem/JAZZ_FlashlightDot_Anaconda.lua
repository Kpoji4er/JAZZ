UndefineClass('JAZZ_FlashlightDot_Anaconda')
DefineClass.JAZZ_FlashlightDot_Anaconda = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laserlight",
	DisplayName = T(990002145, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_Anaconda DisplayName]] "Tactical Device"),
	DisplayNamePlural = T(990002146, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_Anaconda DisplayNamePlural]] "Tactical Device"),
	AdditionalHint = T(990002147, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_Anaconda AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_FlashlightDot_Anaconda",
}
