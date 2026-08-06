UndefineClass('JAZZ_Scope_Scout')
DefineClass.JAZZ_Scope_Scout = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "Mod/e6L4ECj/WeaponComponents/Optics/ScoutScope.png",
	DisplayName = T(990002370, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Scout DisplayName]] "Оптический Прицел Vortex Crossfire II Scout Scope (2-7x)"),
	DisplayNamePlural = T(990002371, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Scout DisplayNamePlural]] "Оптический Прицел Vortex Crossfire II Scout Scope (2-7x)"),
	AdditionalHint = T(990002372, --[[ModItemInventoryItemCompositeDef JAZZ_Scope_Scout AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 10000,
	CanAppearInShop = true,
	RestockWeight = 8,
	MaxStock = 1,
	Tier = 4,
	CategoryPair = "Optics",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Scope_Scout",
}
