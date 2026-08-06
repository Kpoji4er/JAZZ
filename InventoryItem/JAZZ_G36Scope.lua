UndefineClass('JAZZ_G36Scope')
DefineClass.JAZZ_G36Scope = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/g36_scope_02",
	DisplayName = T(990002163, --[[ModItemInventoryItemCompositeDef JAZZ_G36Scope DisplayName]] "Прицел G36 3x"),
	DisplayNamePlural = T(990002164, --[[ModItemInventoryItemCompositeDef JAZZ_G36Scope DisplayNamePlural]] "Прицел G36 3x"),
	AdditionalHint = T(990002165, --[[ModItemInventoryItemCompositeDef JAZZ_G36Scope AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 0,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_G36Scope",
}
