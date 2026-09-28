UndefineClass('JAZZ_VerticalGrip_M14')
DefineClass.JAZZ_VerticalGrip_M14 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_VerticalGrip_M14",
	object_class = "JAZZ_RemovableAttachment",
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002421, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002422, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002423, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_M14 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 28,
	CategoryPair = "Under",
}

