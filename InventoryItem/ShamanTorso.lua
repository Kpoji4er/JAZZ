UndefineClass('ShamanTorso')
DefineClass.ShamanTorso = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 16,
	Icon = "UI/Icons/Items/shaman_armor",
	DisplayName = T(890006818026, --[[ModItemInventoryItemCompositeDef ShamanTorso DisplayName]] "Броня «Отряда смерти»"),
	DisplayNamePlural = T(153182052241, --[[ModItemInventoryItemCompositeDef ShamanTorso DisplayNamePlural]] "Броня «Отряда смерти»"),
	Description = T(730568971680, --[[ModItemInventoryItemCompositeDef ShamanTorso Description]] 'Тяжелый штурмовой бронежилет шамана Сангомы, который он носил в бытностью свою ликвидатором этого их "Отряда Смерти", что заметно по характерной устрашающей раскраске. Интересно, что на бронежилете нет никаких следов от пуль или осколков, можно сказать - не битый, не крашеный.'),
	AdditionalHint = "",
	Valuable = 1,
	RestockWeight = 0,
	PenetrationClass = 4,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Arms", "Groin", "Torso" ),
	ArmorRating = 20,
	MeleeArmorRating = 30,
	ExplosiveArmorRating = 100,
	CanHoldPlate = true,
	Weight = 4,
	SuppressionProtection = 35,
}

