UndefineClass('JazzArmor_UHMWPEHelm')
DefineClass.JazzArmor_UHMWPEHelm = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/UHMWPEHelm.png",
	DisplayName = T(809599322813, "Шлем СВМПЭ"),
	DisplayNamePlural = T(647571118464, "Шлемы СВМПЭ"),
	Description = T(524823952227, "Современный защитный шлем из сверхплотного высокомолекулярного полиэтилена (СВМПЭ). Производителем заявляется, что шлемы рекомендованы для проведения Ночных Операций."),
	AdditionalHint = T(880747947165, "Защитный шлем из сверхплотного высокомолекулярного полиэтилена"),
	Valuable = 1,
	Cost = 25000,
	CanAppearInShop = true,
	RestockWeight = 0,
	CategoryPair = "Heavy",
	Slot = "Head",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head", "Neck" ),
	Coverage = 80,
	ArmorRating = 32,
	MeleeArmorRating = 10,
	Weight = 4,
	ArmorResource = 400,
	Repairability = 45,
}

