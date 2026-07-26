UndefineClass('FlakArmor')
DefineClass.FlakArmor = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_armor",
	DisplayName = T(562131155592, --[[ModItemInventoryItemCompositeDef FlakArmor DisplayName]] "Flak Armor"),
	DisplayNamePlural = T(259150406513, --[[ModItemInventoryItemCompositeDef FlakArmor DisplayNamePlural]] "Flak Armors"),
	Cost = 1200,
	MaxStock = 2,
	RestockWeight = 75,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

