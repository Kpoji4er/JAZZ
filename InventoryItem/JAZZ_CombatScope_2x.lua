UndefineClass('JAZZ_CombatScope_2x')
DefineClass.JAZZ_CombatScope_2x = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_CombatScope_2x",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_CombatScope_2x",
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/2x.png",
	DisplayName = T(990002118, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_2x DisplayName]] "Штурмовой прицел (2x)"),
	DisplayNamePlural = T(990002119, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_2x DisplayNamePlural]] "Штурмовой прицел (2x)"),
	AdditionalHint = T(990002120, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_2x AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "Optics",
}

