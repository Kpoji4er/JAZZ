UndefineClass('JAZZ_Reflex_PKAS')
DefineClass.JAZZ_Reflex_PKAS = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/PKAS.png",
	DisplayName = T(990002337, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_PKAS DisplayName]] "Коллиматор ПК-АА"),
	DisplayNamePlural = T(990002338, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_PKAS DisplayNamePlural]] "Коллиматор ПК-АА"),
	AdditionalHint = T(990002339, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_PKAS AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_PKAS",
}
