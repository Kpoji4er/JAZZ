UndefineClass('JAZZ_ArmorUpgrade')
DefineClass.JAZZ_ArmorUpgrade = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/combination_weave_padding",
	DisplayName = T(479526429789, "Комплект Дополнительного бронирования"),
	DisplayNamePlural = T(191364946234, "Комплекты Дополнительного бронирования"),
	AdditionalHint = T(901500357188, "Используются чтобы повысить класс защиты у модульных бронежилетов"),
	Cost = 5000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 15,
	CategoryPair = "Components",
}

