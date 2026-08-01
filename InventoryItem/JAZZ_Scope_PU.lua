UndefineClass('JAZZ_Scope_PU')
DefineClass.JAZZ_Scope_PU = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/PUScope.png",
	DisplayName = T(990002367, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PU DisplayName]] "Оптический Прицел ПУ (3.5x)"),
	DisplayNamePlural = T(990002368, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PU DisplayNamePlural]] "Оптический Прицел ПУ (3.5x)"),
	AdditionalHint = T(990002369, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PU AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Scope_PU",
}
