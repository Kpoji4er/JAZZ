UndefineClass('KevlarVest')
DefineClass.KevlarVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_armor",
	DisplayName = T(681283668250, --[[ModItemInventoryItemCompositeDef KevlarVest DisplayName]] "Kevlar Armor"),
	DisplayNamePlural = T(520688450583, --[[ModItemInventoryItemCompositeDef KevlarVest DisplayNamePlural]] "Kevlar Armors"),
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

