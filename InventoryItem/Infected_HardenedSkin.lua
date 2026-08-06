UndefineClass('Infected_HardenedSkin')
DefineClass.Infected_HardenedSkin = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 3,
	RepairCost = 1000,
	CanAppearInShop = false,
	Repairable = false,
	Degradation = 0,
	Icon = "UI/Icons/Items/kevlar_vest",
	DisplayName = T(963293413235, --[[ModItemInventoryItemCompositeDef Infected_HardenedSkin DisplayName]] "Resilience"),
	DisplayNamePlural = T(466287168405, --[[ModItemInventoryItemCompositeDef Infected_HardenedSkin DisplayNamePlural]] "Resilience"),
	Description = "",
	AdditionalHint = "",
	Cost = 4800,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	DamageReduction = 0,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Arms", "Groin", "Legs", "Torso" ),
	ArmorRating = 100,
	MeleeArmorRating = 100,
	StunGrenadeProtection = 100,
}

