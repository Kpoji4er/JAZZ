UndefineClass('JAZZ_FlashlightDot')
DefineClass.JAZZ_FlashlightDot = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_FlashlightDot",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/side_laserlight",
	DisplayName = T(990002142, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot DisplayName]] "Tactical Device"),
	DisplayNamePlural = T(990002143, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot DisplayNamePlural]] "Tactical Device"),
	AdditionalHint = T(990002144, --[[ModItemInventoryItemCompositeDef JAZZ_FlashlightDot AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Side",
}

