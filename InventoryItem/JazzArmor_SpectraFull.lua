UndefineClass('JazzArmor_SpectraFull')
DefineClass.JazzArmor_SpectraFull = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 H T5",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "Mod/e6L4ECj/ArmorIcons/SpectraH.png",
	DisplayName = T(213775254543, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraFull DisplayName]] "Бронежилет СПЕКТРА, Тяжелый"),
	DisplayNamePlural = T(853661630706, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraFull DisplayNamePlural]] "Бронежилеты СПЕКТРА, Тяжелый"),
	Description = T(259769536367, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraFull Description]] "Современный и даже футуристичный бронежилет СПЕКТРА был захвачен в качестве трофея Ассоциацией во время операции в Арулько. Каким-то неизвестным нам образом (Ассоциация абсолютно точно не имеет к этому никакого отношения) он попал на черный рынок, откуда смог распространиться по всему миру. Производитель - неизвестен. Защита - как у танка. Тяжелый штурмовой вариант с защитой шеи, паха и рук."),
	AdditionalHint = T(462973165184, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraFull AdditionalHint]] "Бронежилет универсального солдата. Штурмовой вариант"),
	Cost = 250000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 5,
	CategoryPair = "Heavy",
	PenetrationClass = 4,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Neck", "Torso" ),
	ArmorRating = 25,
	MeleeArmorRating = 40,
	ExplosiveArmorRating = 50,
	CanHoldPlate = true,
	Weight = 4,
	SuppressionProtection = 35,
}

