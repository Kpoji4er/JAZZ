UndefineClass('JAZZ_CombatScope_ACOG')
DefineClass.JAZZ_CombatScope_ACOG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ACOG.png",
	DisplayName = T(990002124, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG DisplayName]] "Штурмовой прицел ACOG (4x)"),
	DisplayNamePlural = T(990002125, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG DisplayNamePlural]] "Штурмовой прицел ACOG (4x)"),
	AdditionalHint = T(990002126, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_CombatScope_ACOG",
}
