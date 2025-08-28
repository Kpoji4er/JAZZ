UndefineClass('JazzArmor_BallisticMask')
DefineClass.JazzArmor_BallisticMask = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "Mod/e6L4ECj/ArmorIcons/BallisticMask.png",
	DisplayName = T(521466489826, "Кевларовая маска"),
	DisplayNamePlural = T(418143378072, "Кевларовые маски"),
	Description = T(245284644888, "Баллистическая защитная маска с прорезями для глаз. По задумке, должна защищать хозяина от выстрелов в лицо. Я бы на вашем месте не проверял."),
	AdditionalHint = T(488942668336, "Кевларовая защита для лица"),
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 5,
	Slot = "HeadGear",
	PenetrationClass = 2,
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 20,
	ArmorRating = 10,
	Weight = 2,
	Vision = -10,
	StunGrenadeProtection = 5,
	ArmorResource = 180,
}

