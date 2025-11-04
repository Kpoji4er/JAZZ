UndefineClass('JazzArmor_RaiderKneePads')
DefineClass.JazzArmor_RaiderKneePads = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 L",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 70,
	Icon = "Mod/e6L4ECj/ArmorIcons/RaiderPads.png",
	DisplayName = T(127339604026, --[[ModItemInventoryItemCompositeDef JazzArmor_RaiderKneePads DisplayName]] "Рейдерские наколенники"),
	DisplayNamePlural = T(855397811441, --[[ModItemInventoryItemCompositeDef JazzArmor_RaiderKneePads DisplayNamePlural]] "Рейдерские наколенники"),
	Description = T(974243239899, --[[ModItemInventoryItemCompositeDef JazzArmor_RaiderKneePads Description]] 'Защита коленей, спроектированная и исполненная тем же безумным дизайнером брони Легиона, что ответственнен за такие шедевры как "ржавая кольчуга из шин" и "сварной панцирь из автомобильной двери". Ждем нового шедевра - "кираса из дорожных знаков"'),
	AdditionalHint = T(793616271672, --[[ModItemInventoryItemCompositeDef JazzArmor_RaiderKneePads AdditionalHint]] "Самодельные наколенники"),
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 30,
	ArmorRating = 8,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 5,
	Weight = 2,
	ArmorResource = 250,
	Repairability = 95,
}

