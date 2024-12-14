UndefineClass('JazzArmor_RBA')
DefineClass.JazzArmor_RBA = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 L T3",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 25,
	Icon = "Mod/e6L4ECj/ArmorIcons/RBA.png",
	DisplayName = T(920136799882, --[[ModItemInventoryItemCompositeDef JazzArmor_RBA DisplayName]] 'Бронежилет "Рейнджер"'),
	DisplayNamePlural = T(782346732353, --[[ModItemInventoryItemCompositeDef JazzArmor_RBA DisplayNamePlural]] 'Бронежилет "Рейнджер"'),
	Description = T(442215590616, --[[ModItemInventoryItemCompositeDef JazzArmor_RBA Description]] 'Бронежилет знаменитых "рейнджеров" Армии США. Гибкие кевларовые панели совмещаются с пулестойкими керамическими пластинами, что в совокупности дает бойцу неплохую защищенность и не так сильно ограничивает подвижность.'),
	AdditionalHint = T(214525897697, --[[ModItemInventoryItemCompositeDef JazzArmor_RBA AdditionalHint]] "Американский бронежилет"),
	Cost = 5500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 3,
	CategoryPair = "Light",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 55,
	ArmorRating = 14,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 21,
	CamouflagePercent = 8,
	CanHoldPlate = true,
	Weight = 2,
}

