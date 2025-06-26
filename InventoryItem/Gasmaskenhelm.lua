UndefineClass('Gasmaskenhelm')
DefineClass.Gasmaskenhelm = {
	__parents = { "GasMaskBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "GasMaskBase",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "UI/Icons/Items/gasmaskenhelm.png",
	DisplayName = T(222746884728, --[[ModItemInventoryItemCompositeDef Gasmaskenhelm DisplayName]] "Gasmaskenhelm"),
	DisplayNamePlural = T(437672891116, --[[ModItemInventoryItemCompositeDef Gasmaskenhelm DisplayNamePlural]] "Gasmaskenhelme"),
	AdditionalHint = T(414353864856, --[[ModItemInventoryItemCompositeDef Gasmaskenhelm AdditionalHint]] "Противогаз и шлем"),
	Tier = 2,
	Slot = "Head",
	PenetrationClass = 4,
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	ArmorRating = 20,
	MeleeArmorRating = 40,
	ExplosiveArmorRating = 50,
	BlockFaceSlot = true,
	Weight = 4,
	NightVision = -10,
	Vision = -10,
	DustStormProtection = 30,
	StunGrenadeProtection = 30,
}

