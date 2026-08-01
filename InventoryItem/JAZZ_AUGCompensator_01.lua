UndefineClass('JAZZ_AUGCompensator_01')
DefineClass.JAZZ_AUGCompensator_01 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/muzzle_steyr_02",
	DisplayName = T(990002100, --[[ModItemInventoryItemCompositeDef JAZZ_AUGCompensator_01 DisplayName]] "Default Compensator"),
	DisplayNamePlural = T(990002101, --[[ModItemInventoryItemCompositeDef JAZZ_AUGCompensator_01 DisplayNamePlural]] "Default Compensator"),
	AdditionalHint = T(990002102, --[[ModItemInventoryItemCompositeDef JAZZ_AUGCompensator_01 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1000,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_AUGCompensator_01",
}
