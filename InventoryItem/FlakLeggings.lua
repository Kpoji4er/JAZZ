UndefineClass('FlakLeggings')
DefineClass.FlakLeggings = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_leggings",
	DisplayName = T(491297757952, --[[ModItemInventoryItemCompositeDef FlakLeggings DisplayName]] "Flak Leggings"),
	DisplayNamePlural = T(547653505048, --[[ModItemInventoryItemCompositeDef FlakLeggings DisplayNamePlural]] "Flak Leggings"),
	Cost = 800,
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Legs",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

