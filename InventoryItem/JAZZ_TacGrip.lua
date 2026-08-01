UndefineClass('JAZZ_TacGrip')
DefineClass.JAZZ_TacGrip = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002391, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip DisplayName]] "Tactical Grip"),
	DisplayNamePlural = T(990002392, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip DisplayNamePlural]] "Tactical Grip"),
	AdditionalHint = T(990002393, --[[ModItemInventoryItemCompositeDef JAZZ_TacGrip AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_TacGrip",
}
