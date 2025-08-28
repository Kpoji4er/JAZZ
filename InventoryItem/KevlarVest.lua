UndefineClass('KevlarVest')
DefineClass.KevlarVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_armor",
	DisplayName = T(939389846992, "Кевларовая броня"),
	DisplayNamePlural = T(102906812460, "Кевларовая броня"),
	Cost = 2800,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 50,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

