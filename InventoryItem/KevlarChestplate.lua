UndefineClass('KevlarChestplate')
DefineClass.KevlarChestplate = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_vest",
	DisplayName = T(385029395380, "Кевларовый жилет"),
	DisplayNamePlural = T(970450020508, "Кевларовые жилеты"),
	Cost = 1400,
	Tier = 2,
	RestockWeight = 50,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
}

