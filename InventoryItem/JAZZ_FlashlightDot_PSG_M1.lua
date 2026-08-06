UndefineClass('JAZZ_FlashlightDot_PSG_M1')
DefineClass.JAZZ_FlashlightDot_PSG_M1 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/side_laserlight",
	DisplayName = T(990002148, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_PSG_M1 DisplayName]] "Tactical Device"),
	DisplayNamePlural = T(990002149, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_PSG_M1 DisplayNamePlural]] "Tactical Device"),
	AdditionalHint = T(990002150, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot_PSG_M1 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = true,
	RestockWeight = 5,
	MaxStock = 1,
	Tier = 5,
	CategoryPair = "Side",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_FlashlightDot_PSG_M1",
}
