UndefineClass('JAZZ_FlashlightDot')
DefineClass.JAZZ_FlashlightDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laserlight",
	DisplayName = T(990002142, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot DisplayName]] "Tactical Device"),
	DisplayNamePlural = T(990002143, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot DisplayNamePlural]] "Tactical Device"),
	AdditionalHint = T(990002144, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = true,
	RestockWeight = 28,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_FlashlightDot",
}
