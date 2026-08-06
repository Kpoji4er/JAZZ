UndefineClass('JAZZ_Scope_PSO')
DefineClass.JAZZ_Scope_PSO = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/PSO.png",
	DisplayName = T(990002364, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PSO DisplayName]] "Оптический Прицел ПСО (4x)"),
	DisplayNamePlural = T(990002365, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PSO DisplayNamePlural]] "Оптический Прицел ПСО (4x)"),
	AdditionalHint = T(990002366, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_PSO AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 6000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Scope_PSO",
}
