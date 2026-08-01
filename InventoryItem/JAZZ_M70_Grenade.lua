UndefineClass('JAZZ_M70_Grenade')
DefineClass.JAZZ_M70_Grenade = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/parts_placeholder",
	DisplayName = T(990002208, --[[ModItemInventoryItemCompositeDef JAZZ_M70_Grenade DisplayName]] "Наствольная граната для М70"),
	DisplayNamePlural = T(990002209, --[[ModItemInventoryItemCompositeDef JAZZ_M70_Grenade DisplayNamePlural]] "Наствольная граната для М70"),
	AdditionalHint = T(990002210, --[[ModItemInventoryItemCompositeDef JAZZ_M70_Grenade AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 0,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_M70_Grenade",
}
