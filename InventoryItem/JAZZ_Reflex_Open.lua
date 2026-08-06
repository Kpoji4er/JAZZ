UndefineClass('JAZZ_Reflex_Open')
DefineClass.JAZZ_Reflex_Open = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ReflexOpen.png",
	DisplayName = T(990002334, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open DisplayName]] "Коллиматор Компактный"),
	DisplayNamePlural = T(990002335, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open DisplayNamePlural]] "Коллиматор Компактный"),
	AdditionalHint = T(990002336, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Open AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 28,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Optics",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Open",
}
