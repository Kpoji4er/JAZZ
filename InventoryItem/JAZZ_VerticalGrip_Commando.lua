UndefineClass('JAZZ_VerticalGrip_Commando')
DefineClass.JAZZ_VerticalGrip_Commando = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "WEAPONS-002 remountable → component JAZZ_VerticalGrip_Commando",
	object_class = "JAZZ_RemovableAttachment",
	RemovableComponentId = "JAZZ_VerticalGrip_Commando",
	Icon = "UI/Icons/Upgrades/mp5_grip",
	DisplayName = T(990002418, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando DisplayName]] "Vertical Grip"),
	DisplayNamePlural = T(990002419, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando DisplayNamePlural]] "Vertical Grip"),
	AdditionalHint = T(990002420, --[[ModItemInventoryItemCompositeDef JAZZ_VerticalGrip_Commando AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Components",
}

