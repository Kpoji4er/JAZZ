UndefineClass('JAZZ_Reflex_Open')
DefineClass.JAZZ_Reflex_Open = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_Reflex_Open",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_Reflex_Open",
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ReflexOpen.png",
	DisplayName = T(990002334, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open DisplayName]] "Коллиматор Компактный"),
	DisplayNamePlural = T(990002335, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open DisplayNamePlural]] "Коллиматор Компактный"),
	AdditionalHint = T(990002336, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Optics",
}

