UndefineClass('FlakVest')
DefineClass.FlakVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_vest",
	DisplayName = T(238942815086, --[[ModItemInventoryItemCompositeDef FlakVest DisplayName]] "Flak Vest"),
	DisplayNamePlural = T(383155432380, --[[ModItemInventoryItemCompositeDef FlakVest DisplayNamePlural]] "Flak Vests"),
	Cost = 800,
	RestockWeight = 75,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
}

