UndefineClass('JAZZ_Reflex_Eotech')
DefineClass.JAZZ_Reflex_Eotech = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/Eotech.png",
	DisplayName = T(990002325, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech DisplayName]] "Коллиматор Eotech"),
	DisplayNamePlural = T(990002326, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech DisplayNamePlural]] "Коллиматор Eotech"),
	AdditionalHint = T(990002327, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 9000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Eotech",
}
