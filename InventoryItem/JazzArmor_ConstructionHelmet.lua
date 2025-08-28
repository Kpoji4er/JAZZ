UndefineClass('JazzArmor_ConstructionHelmet')
DefineClass.JazzArmor_ConstructionHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 L",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 30,
	Icon = "Mod/e6L4ECj/ArmorIcons/ConstructionHelmet.png",
	DisplayName = T(173223273387, "Строительная каска"),
	DisplayNamePlural = T(654274057334, "Строительные каски"),
	Description = T(942790476830, "Яркая желтая строительная каска. Может защитить от удара по голове тупым и тяжелым предметом произвольной формы."),
	AdditionalHint = "",
	Valuable = 1,
	Cost = 100,
	CanAppearInShop = true,
	RestockWeight = 1,
	Slot = "Head",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Head" ),
	Coverage = 50,
	ArmorRating = 8,
	MeleeArmorRating = 24,
	CamouflagePercent = -8,
	Weight = 2,
	ArmorResource = 80,
	Repairability = 80,
}

