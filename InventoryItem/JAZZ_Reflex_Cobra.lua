UndefineClass('JAZZ_Reflex_Cobra')
DefineClass.JAZZ_Reflex_Cobra = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/Kobra.png",
	DisplayName = T(990002322, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Cobra DisplayName]] "Коллиматор Кобра"),
	DisplayNamePlural = T(990002323, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Cobra DisplayNamePlural]] "Коллиматор Кобра"),
	AdditionalHint = T(990002324, --[[ModItemInventoryItemCompositeDef JAZZ_Reflex_Cobra AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 3500,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Optics",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Reflex_Cobra",
}
