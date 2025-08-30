UndefineClass('JazzArmor_UHMWPEFull')
DefineClass.JazzArmor_UHMWPEFull = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 H T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/UHMWPEFull.png",
	DisplayName = T(197372367064, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPEFull DisplayName]] "Бронежилет СВМПЭ, Тяжелый"),
	DisplayNamePlural = T(379319464770, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPEFull DisplayNamePlural]] "Бронежилеты СВМПЭ, Тяжелые"),
	Description = T(960851086720, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPEFull Description]] "Тяжелый штурмовой бронежилет с защитой паха и рук из сверхплотного высокомолекулярного полиэтилена (СВМПЭ). Производитель предлагал Ассоциации эксклюзивный контракт, но мы были вынуждены отказаться, из за странного условия - провести необходимое количество Ночных Операций."),
	AdditionalHint = T(779848171279, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPEFull AdditionalHint]] "Бронежилет из сверхплотного высокомолекулярного полиэтилена. Штурмовой вариант"),
	Cost = 75000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	PenetrationClass = 4,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Torso" ),
	Coverage = 85,
	ArmorRating = 18,
	MeleeArmorRating = 30,
	ExplosiveArmorRating = 70,
	CanHoldPlate = true,
	Weight = 4,
	ArmorResource = 650,
	Repairability = 45,
}

