UndefineClass('JazzArmor_EOD')
DefineClass.JazzArmor_EOD = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 N T2 !!!",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 75,
	Icon = "Mod/e6L4ECj/ArmorIcons/EOD.png",
	DisplayName = T(890000000014200, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayName]] "Бронежилет EOD"),
	DisplayNamePlural = T(890000000014201, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD DisplayNamePlural]] "Бронежилеты EOD"),
	Description = T(890000000014202, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD Description]] "Тяжёлый сапёрный бронежилет для работ по разминированию. Толстые противоосколочные пакеты и высокий воротник хорошо держат взрывную волну, но от винтовочной пули толку мало, а сам жилет ощутимо тяжёлый."),
	AdditionalHint = T(890000000014203, --[[ModItemInventoryItemCompositeDef JazzArmor_EOD AdditionalHint]] "Броня для разминирования"),
	Cost = 8500,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 55,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 15,
	MeleeArmorRating = 50,
	ExplosiveArmorRating = 100,
	CamouflagePercent = 3,
	Weight = 5,
	ArmorResource = 180,
	Repairability = 65,
}

