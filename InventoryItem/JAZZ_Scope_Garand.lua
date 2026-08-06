UndefineClass('JAZZ_Scope_Garand')
DefineClass.JAZZ_Scope_Garand = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/GarandScope.png",
	DisplayName = T(990002358, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Garand DisplayName]] "Оптический Прицел M84 (2.2x)"),
	DisplayNamePlural = T(990002359, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Garand DisplayNamePlural]] "Оптический Прицел M84 (2.2x)"),
	AdditionalHint = T(990002360, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Garand AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 4000,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Scope_Garand",
}
