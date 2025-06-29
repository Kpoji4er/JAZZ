UndefineClass('JazzArmor_ImprovisedCuirass')
DefineClass.JazzArmor_ImprovisedCuirass = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 H T1",
	object_class = "Armor",
	ScrapParts = 4,
	Icon = "Mod/e6L4ECj/ArmorIcons/ImprovisedCuirass.png",
	DisplayName = T(360726472475, --[[ModItemInventoryItemCompositeDef JazzArmor_ImprovisedCuirass DisplayName]] "Самодельная кираса"),
	DisplayNamePlural = T(912113361221, --[[ModItemInventoryItemCompositeDef JazzArmor_ImprovisedCuirass DisplayNamePlural]] "Самодельные кирасы"),
	Description = T(476224341686, --[[ModItemInventoryItemCompositeDef JazzArmor_ImprovisedCuirass Description]] 'Самодельная кираса из листового железа "Мейд бай Легион". По задумке, должна защищать тяжелого бойца Легиона от винтовочного и пулеметного огня. Главное, чтоб тяжелый боец Легиона в это верил.'),
	AdditionalHint = T(168857410077, --[[ModItemInventoryItemCompositeDef JazzArmor_ImprovisedCuirass AdditionalHint]] "Самодельная кираса, сваренная из листов железа и обшитая кожей"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Coverage = 50,
	ArmorRating = 18,
	MeleeArmorRating = 30,
	ExplosiveArmorRating = 25,
	CamouflagePercent = -15,
	Weight = 4,
	ArmorResource = 700,
	Repairability = 95,
}

