UndefineClass('JAZZ_SuppressorIntegrated')
DefineClass.JAZZ_SuppressorIntegrated = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/beretta_silencer",
	DisplayName = T(990002388, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorIntegrated DisplayName]] "Глушитель Интегрированный"),
	DisplayNamePlural = T(990002389, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorIntegrated DisplayNamePlural]] "Глушитель Интегрированный"),
	AdditionalHint = T(990002390, --[[ModItemInventoryItemCompositeDef JAZZ_SuppressorIntegrated AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = false,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_SuppressorIntegrated",
}
