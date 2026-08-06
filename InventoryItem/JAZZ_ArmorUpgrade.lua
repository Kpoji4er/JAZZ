UndefineClass('JAZZ_ArmorUpgrade')
DefineClass.JAZZ_ArmorUpgrade = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/combination_weave_padding",
	DisplayName = T(479526429789, --[[ModItemInventoryItemCompositeDef JAZZ_ArmorUpgrade DisplayName]] "Комплект Дополнительного бронирования"),
	DisplayNamePlural = T(191364946234, --[[ModItemInventoryItemCompositeDef JAZZ_ArmorUpgrade DisplayNamePlural]] "Комплекты Дополнительного бронирования"),
	AdditionalHint = T(901500357188, --[[ModItemInventoryItemCompositeDef JAZZ_ArmorUpgrade AdditionalHint]] "Используются чтобы повысить класс защиты у модульных бронежилетов"),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 80,
	CategoryPair = "Components",
}

