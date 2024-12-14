UndefineClass('FlakVest')
DefineClass.FlakVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_vest",
	DisplayName = T(260264257341, --[[ModItemInventoryItemCompositeDef FlakVest DisplayName]] "Противооскол. жилет"),
	DisplayNamePlural = T(881781038796, --[[ModItemInventoryItemCompositeDef FlakVest DisplayNamePlural]] "Противооскол. жилеты"),
	Cost = 800,
	RestockWeight = 75,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
}

