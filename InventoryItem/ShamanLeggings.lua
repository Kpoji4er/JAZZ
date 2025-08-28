UndefineClass('ShamanLeggings')
DefineClass.ShamanLeggings = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 16,
	Icon = "UI/Icons/Items/shaman_leggings",
	DisplayName = T(120730773488, "Поножи «Отряда смерти»"),
	DisplayNamePlural = T(631889042724, "Поножи «Отряда смерти»"),
	Description = T(252226201975, 'Личные бронештаны шамана Сангомы, которые он использовал еще в "Отряде Смерти". Надеюсь, он хотя бы их потом стирал.'),
	AdditionalHint = "",
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
	ArmorRating = 25,
	MeleeArmorRating = 30,
	ExplosiveArmorRating = 80,
	Weight = 3,
	ArmorResource = 350,
	Repairability = 85,
}

