UndefineClass('JazzArmor_SpectraLegs')
DefineClass.JazzArmor_SpectraLegs = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class4 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 32,
	Icon = "Mod/e6L4ECj/ArmorIcons/SpectraLegs.png",
	DisplayName = T(518221619774, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraLegs DisplayName]] "Штаны Спектра"),
	DisplayNamePlural = T(734743271825, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraLegs DisplayNamePlural]] "Штаны Спектра"),
	Description = T(795682654372, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraLegs Description]] 'Футуристичная "универсальная броня солдата", или, как она более известна, броня СПЕКТРА, в огромном количестве попала на черный рынок после операции Ассоциации в Арулько. Изготовленные из этого материала поножи обеспечивают серьезный уровень защиты для ног бойца.'),
	AdditionalHint = T(488169984563, --[[ModItemInventoryItemCompositeDef JazzArmor_SpectraLegs AdditionalHint]] "Штаны универсального солдата."),
	Valuable = 1,
	Cost = 150000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 3,
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
	Coverage = 90,
	ArmorRating = 20,
	MeleeArmorRating = 40,
	ExplosiveArmorRating = 40,
	Weight = 4,
	ArmorResource = 700,
	Repairability = 30,
}

