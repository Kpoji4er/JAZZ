UndefineClass('JAZZ_MagLarge_10_20_SVD')
DefineClass.JAZZ_MagLarge_10_20_SVD = {
	__parents = { "JAZZ_RemovableAttachment" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	object_class = "JAZZ_RemovableAttachment",
	Repairable = false,
	Icon = "UI/Icons/Upgrades/galil_magazine_large",
	DisplayName = T(990002532, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20_SVD DisplayName]] "Магазин на 20 патрон"),
	DisplayNamePlural = T(990002533, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20_SVD DisplayNamePlural]] "Магазин на 20 патрон"),
	AdditionalHint = T(990002534, --[[ModItemInventoryItemCompositeDef JAZZ_MagLarge_10_20_SVD AdditionalHint]] "Семья магазинов: SVD. Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."),
	Cost = 2500,
	CanAppearInShop = true,
	RestockWeight = 38,
	MaxStock = 1,
	Tier = 2,
	CategoryPair = "Magazines",
	MaxStacks = 1,
	RemovableComponentId = "JAZZ_MagLarge_10_20_SVD",
}
