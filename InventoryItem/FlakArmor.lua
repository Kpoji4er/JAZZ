UndefineClass('FlakArmor')
DefineClass.FlakArmor = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_armor",
	DisplayName = T(361278570973, "Противооскол. броня"),
	DisplayNamePlural = T(146267206767, "Противооскол. броня"),
	Cost = 1200,
	MaxStock = 2,
	RestockWeight = 75,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

