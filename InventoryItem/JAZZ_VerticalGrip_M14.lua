UndefineClass('JAZZ_VerticalGrip_M14')
DefineClass.JAZZ_VerticalGrip_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002421, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002422, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002423, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_VerticalGrip_M14",
}
