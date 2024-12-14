UndefineClass('JazzArmor_UHMWPE')
DefineClass.JazzArmor_UHMWPE = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/UHMWPE.png",
	DisplayName = T(153412761781, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPE DisplayName]] "Бронежилет СВМПЭ"),
	DisplayNamePlural = T(506761784252, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPE DisplayNamePlural]] "Бронежилеты СВМПЭ"),
	Description = T(693364549331, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPE Description]] "Современный коммерческий бронежилет с защитой паха из сверхплотного высокомолекулярного полиэтилена (СВМПЭ). Производитель предлагал Ассоциации эксклюзивный контракт, но мы были вынуждены отказаться, из за странного условия - провести необходимое количество Ночных Операций."),
	AdditionalHint = T(402637516595, --[[ModItemInventoryItemCompositeDef JazzArmor_UHMWPE AdditionalHint]] "Бронежилет из сверхплотного высокомолекулярного полиэтилена."),
	Cost = 50000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 1,
	CategoryPair = "Medium",
	PenetrationClass = 4,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Torso" ),
	Coverage = 75,
	ArmorRating = 14,
	MeleeArmorRating = 10,
	ExplosiveArmorRating = 40,
	CanHoldPlate = true,
	Weight = 3,
}

