UndefineClass('JazzArmor_RaiderMetalLeggins')
DefineClass.JazzArmor_RaiderMetalLeggins = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 H",
	object_class = "Armor",
	ScrapParts = 6,
	Degradation = 60,
	Icon = "Mod/e6L4ECj/ArmorIcons/MetalPads.png",
	DisplayName = T(286138794123, "Самодельные металлические поножи"),
	DisplayNamePlural = T(761509212290, "Самодельные металлические поножи"),
	Description = T(378313906596, "Армированные поножи из сваренного листового металла. Легион беспощаден к своим врагам. На это же невозможно смотреть без смеха."),
	AdditionalHint = T(830578325184, "Тяжелая броня для ног из металла"),
	Valuable = 1,
	RestockWeight = 0,
	Slot = "Legs",
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Legs" ),
	Coverage = 60,
	ArmorRating = 30,
	MeleeArmorRating = 8,
	ExplosiveArmorRating = 10,
	CamouflagePercent = -10,
	Weight = 4,
	ArmorResource = 400,
	Repairability = 95,
}

