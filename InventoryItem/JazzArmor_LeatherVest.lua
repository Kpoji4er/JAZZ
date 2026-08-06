UndefineClass('JazzArmor_LeatherVest')
DefineClass.JazzArmor_LeatherVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 L T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/SleevelessJacket.png",
	DisplayName = T(199686950281, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherVest DisplayName]] "Кожаный жилет"),
	DisplayNamePlural = T(811963761047, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherVest DisplayNamePlural]] "Кожаные жилеты"),
	Description = T(578512789921, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherVest Description]] "Черный байкерский кожаный жилет. Вряд ли Гвоздь согласиться дать примерить. Хотя, учитывая, что байкеры свои жилеты не стирают - не стоит."),
	AdditionalHint = T(796609766807, --[[ModItemInventoryItemCompositeDef JazzArmor_LeatherVest AdditionalHint]] "Черный кожаный жилет"),
	Cost = 250,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 1,
	RestockWeight = 120,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Camouflage = true,
	Coverage = 60,
	ArmorRating = 6,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 5,
	ArmorResource = 40,
	Repairability = 85,
}

