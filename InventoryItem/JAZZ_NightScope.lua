UndefineClass('JAZZ_NightScope')
DefineClass.JAZZ_NightScope = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/NVS.png",
	DisplayName = T(990002304, --[[ModItemInventoryItemCompositeDef JAZZ_NightScope DisplayName]] "Ночной прицел (5х)"),
	DisplayNamePlural = T(990002305, --[[ModItemInventoryItemCompositeDef JAZZ_NightScope DisplayNamePlural]] "Ночной прицел (5х)"),
	AdditionalHint = T(990002306, --[[ModItemInventoryItemCompositeDef JAZZ_NightScope AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_NightScope",
}
