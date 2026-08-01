UndefineClass('JAZZ_TacGrip_M14')
DefineClass.JAZZ_TacGrip_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/tactical_grip",
	DisplayName = T(990002394, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 DisplayName]] "Tactical Grip"),
	DisplayNamePlural = T(990002395, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 DisplayNamePlural]] "Tactical Grip"),
	AdditionalHint = T(990002396, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_TacGrip_M14",
}
