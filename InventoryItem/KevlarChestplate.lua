UndefineClass('KevlarChestplate')
DefineClass.KevlarChestplate = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_vest",
	DisplayName = T(876579930330, --[[ModItemInventoryItemCompositeDef KevlarChestplate DisplayName]] "Kevlar Vest"),
	DisplayNamePlural = T(858599622504, --[[ModItemInventoryItemCompositeDef KevlarChestplate DisplayNamePlural]] "Kevlar Vests"),
	Cost = 1400,
	Tier = 2,
	RestockWeight = 50,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
}

