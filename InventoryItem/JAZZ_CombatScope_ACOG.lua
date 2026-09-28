UndefineClass('JAZZ_CombatScope_ACOG')
DefineClass.JAZZ_CombatScope_ACOG = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_CombatScope_ACOG",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ACOG.png",
	DisplayName = T(990002124, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG DisplayName]] "Штурмовой прицел ACOG (4x)"),
	DisplayNamePlural = T(990002125, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG DisplayNamePlural]] "Штурмовой прицел ACOG (4x)"),
	AdditionalHint = T(990002126, --[[ModItemInventoryItemCompositeDef JAZZ_CombatScope_ACOG AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 18,
	CategoryPair = "Optics",
}

