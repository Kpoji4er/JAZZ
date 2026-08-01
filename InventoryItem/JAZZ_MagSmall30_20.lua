UndefineClass('JAZZ_MagSmall30_20')
DefineClass.JAZZ_MagSmall30_20 = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/mp5_mag_normal",
	DisplayName = T(990002301, --[[ModItemInventoryItemCompositeDef JAZZ_MagSmall30_20 DisplayName]] "Магазин на 20 патрон"),
	DisplayNamePlural = T(990002302, --[[ModItemInventoryItemCompositeDef JAZZ_MagSmall30_20 DisplayNamePlural]] "Магазин на 20 патрон"),
	AdditionalHint = T(990002303, --[[ModItemInventoryItemCompositeDef JAZZ_MagSmall30_20 AdditionalHint]] "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 1500,
	CanAppearInShop = true,
	RestockWeight = 10,
	MaxStock = 1,
	Tier = 1,
	CategoryPair = "Components",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagSmall30_20",
}
