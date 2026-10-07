UndefineClass('JAZZ_TacGrip_M14')
DefineClass.JAZZ_TacGrip_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_TacGrip_M14",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_TacGrip_M14",
	Icon = "UI/Icons/Upgrades/tactical_grip",
	DisplayName = T(990002394, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 DisplayName]] "Tactical Grip"),
	DisplayNamePlural = T(990002395, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 DisplayNamePlural]] "Tactical Grip"),
	AdditionalHint = T(990002396, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Under",
}

