UndefineClass('FlakLeggings')
DefineClass.FlakLeggings = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_leggings",
	DisplayName = T(588785070133, --[[ModItemInventoryItemCompositeDef FlakLeggings DisplayName]] "Противооскол. поножи"),
	DisplayNamePlural = T(351261449640, --[[ModItemInventoryItemCompositeDef FlakLeggings DisplayNamePlural]] "Противооскол. поножи"),
	Cost = 800,
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Legs",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

