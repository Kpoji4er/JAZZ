UndefineClass('JazzArmor_AssaultCuirass')
DefineClass.JazzArmor_AssaultCuirass = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 H T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 60,
	Icon = "Mod/e6L4ECj/ArmorIcons/GermanArmor.png",
	DisplayName = T(227560954614, --[[ModItemInventoryItemCompositeDef JazzArmor_AssaultCuirass DisplayName]] "Немецкая штурмовая кираса"),
	DisplayNamePlural = T(943107181623, --[[ModItemInventoryItemCompositeDef JazzArmor_AssaultCuirass DisplayNamePlural]] "Немецкие штурмовые кирасы"),
	Description = T(835746245379, --[[ModItemInventoryItemCompositeDef JazzArmor_AssaultCuirass Description]] 'Сумрачный тевтонский гений еще в Первую Мировую войну придумал снаряжать специальные саперно-штурмовые бригады, вооруженные короткими карабинами, мешком гранат, и вот такими супертяжелыми кирасами. Этакий прообраз "джаггернаута". Штурмовики доказали свою эффективность на полях сражений, но в дальнейшем от расходования 20кг стали на бойца Германия отказалась.'),
	AdditionalHint = T(880788337220, --[[ModItemInventoryItemCompositeDef JazzArmor_AssaultCuirass AdditionalHint]] "Штурмовая кираса времен мировой войны"),
	Cost = 1400,
	CanAppearInShop = false,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Groin", "Torso" ),
	Coverage = 70,
	ArmorRating = 36,
	MeleeArmorRating = 75,
	ExplosiveArmorRating = 40,
	CamouflagePercent = -15,
	Weight = 4,
	ArmorResource = 400,
}

