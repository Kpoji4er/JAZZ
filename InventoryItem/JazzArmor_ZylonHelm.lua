UndefineClass('JazzArmor_ZylonHelm')
DefineClass.JazzArmor_ZylonHelm = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 M",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/ZylonHelm.png",
	DisplayName = T(793998679801, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonHelm DisplayName]] "Шлем Зилон"),
	DisplayNamePlural = T(563910998625, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonHelm DisplayNamePlural]] "Шлемы Зилон"),
	Description = T(960883670355, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonHelm Description]] "Коммерческий шлем из зилона (зайлона) - еще одного типа арамидного волокна. По слухам, хоть зилон и является более прочным, чем кевлар, он быстро теряет защитные свойства со временем."),
	AdditionalHint = T(590407040836, --[[ModItemInventoryItemCompositeDef JazzArmor_ZylonHelm AdditionalHint]] "Модульный камуфляжный шлем"),
	Valuable = 1,
	Cost = 2500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 15,
	CategoryPair = "Medium",
	Slot = "Head",
	PenetrationClass = 2,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 70,
	ArmorRating = 28,
	CamouflagePercent = 3,
	Weight = 3,
}

