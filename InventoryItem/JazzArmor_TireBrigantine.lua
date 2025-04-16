UndefineClass('JazzArmor_TireBrigantine')
DefineClass.JazzArmor_TireBrigantine = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 M T1",
	object_class = "Armor",
	ScrapParts = 4,
	Icon = "Mod/e6L4ECj/ArmorIcons/TireBrigantine.png",
	DisplayName = T(526369699564, --[[ModItemInventoryItemCompositeDef JazzArmor_TireBrigantine DisplayName]] "Самодельная бригантина"),
	DisplayNamePlural = T(249494808285, --[[ModItemInventoryItemCompositeDef JazzArmor_TireBrigantine DisplayNamePlural]] "Самодельные бригантины"),
	Description = T(573274131078, --[[ModItemInventoryItemCompositeDef JazzArmor_TireBrigantine Description]] "Легкая (относительно) бригантина из обрезков шин, используемая подвижными подразделениями Легиона. Ладно хоть в красный не покрасили."),
	AdditionalHint = T(140035693819, --[[ModItemInventoryItemCompositeDef JazzArmor_TireBrigantine AdditionalHint]] "Самодельная бригантина из кольчуги и обрезков шин"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 70,
	ArmorRating = 8,
	MeleeArmorRating = 25,
	ExplosiveArmorRating = 10,
	CamouflagePercent = -15,
	CanHoldPlate = true,
	Weight = 3,
	SuppressionProtection = 10,
}

