UndefineClass('JAZZ_Reflex_Eotech')
DefineClass.JAZZ_Reflex_Eotech = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Reflex_Eotech",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_Reflex_Eotech",
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/Eotech.png",
	DisplayName = T(990002325, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech DisplayName]] "Коллиматор Eotech"),
	DisplayNamePlural = T(990002326, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech DisplayNamePlural]] "Коллиматор Eotech"),
	AdditionalHint = T(990002327, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Eotech AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 9000,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 1,
	RestockWeight = 8,
	CategoryPair = "Optics",
}

