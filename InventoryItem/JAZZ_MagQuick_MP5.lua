UndefineClass('JAZZ_MagQuick_MP5')
DefineClass.JAZZ_MagQuick_MP5 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_quick",
	DisplayName = T(990002616, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_MP5 DisplayName]] "Quick Mag"),
	DisplayNamePlural = T(990002617, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_MP5 DisplayNamePlural]] "Quick Mag"),
	AdditionalHint = T(990002618, --[[ModItemInventoryItemCompositeDef JAZZ_MagQuick_MP5 AdditionalHint]] "Семья магазинов: MP5. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 18,
	MaxStock = 1,
	Tier = 3,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagQuick_MP5",
}
