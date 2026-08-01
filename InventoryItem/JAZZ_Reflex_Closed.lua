UndefineClass('JAZZ_Reflex_Closed')
DefineClass.JAZZ_Reflex_Closed = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/Reflex.png",
	DisplayName = T(990002319, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Closed DisplayName]] "Коллиматор Закрытый"),
	DisplayNamePlural = T(990002320, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Closed DisplayNamePlural]] "Коллиматор Закрытый"),
	AdditionalHint = T(990002321, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Closed AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 5000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Closed",
}
