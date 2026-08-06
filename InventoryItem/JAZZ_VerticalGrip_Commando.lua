UndefineClass('JAZZ_VerticalGrip_Commando')
DefineClass.JAZZ_VerticalGrip_Commando = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002418, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002419, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002420, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = false,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_VerticalGrip_Commando",
}
