UndefineClass('JAZZ_Galil_Brake_Default')
DefineClass.JAZZ_Galil_Brake_Default = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/default_muzzle",
	DisplayName = T(990002172, --[[ModItemInventoryItemCompositeDef JAZZ_Galil_Brake_Default DisplayName]] "Default Muzzle Brake"),
	DisplayNamePlural = T(990002173, --[[ModItemInventoryItemCompositeDef JAZZ_Galil_Brake_Default DisplayNamePlural]] "Default Muzzle Brake"),
	AdditionalHint = T(990002174, --[[ModItemInventoryItemCompositeDef JAZZ_Galil_Brake_Default AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 200,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Muzzle",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_Galil_Brake_Default",
}
