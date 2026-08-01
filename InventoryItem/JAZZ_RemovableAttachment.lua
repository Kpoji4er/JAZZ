UndefineClass('JAZZ_RemovableAttachment')
DefineClass.JAZZ_RemovableAttachment = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/parts_placeholder",
	DisplayName = T(990002005, --[[ModItemInventoryItemCompositeDef JAZZ_RemovableAttachment DisplayName]] "Съёмный оружейный модуль"),
	DisplayNamePlural = T(990002006, --[[ModItemInventoryItemCompositeDef JAZZ_RemovableAttachment DisplayNamePlural]] "Съёмные оружейные модули"),
	AdditionalHint = T(990002007, --[[ModItemInventoryItemCompositeDef JAZZ_RemovableAttachment AdditionalHint]] "Устанавливается на совместимое оружие в кабинете модификации."),
	CanAppearInShop = false,
	MaxStacks = 1,
}
