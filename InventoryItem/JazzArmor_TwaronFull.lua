UndefineClass('JazzArmor_TwaronFull')
DefineClass.JazzArmor_TwaronFull = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class3 M T4",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 15,
	Icon = "Mod/e6L4ECj/ArmorIcons/TwaronH.png",
	DisplayName = T(526646910743, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronFull DisplayName]] "Бронежилет Тварон, Тяжелый"),
	DisplayNamePlural = T(772376898249, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronFull DisplayNamePlural]] "Бронежилеты Тварон, Тяжелые"),
	Description = T(895703383900, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronFull Description]] "Тяжелый штурмовой бронежилет из тварона с дополнительной защитой шеи, рук и паха. Чуть хуже защищает от пуль и осколков, но лучше смягчает удары холодным оружием, что в условиях массированого применения специальных юнитов ближнего боя (дрессированых гиен) Легионом тоже очень важно."),
	AdditionalHint = T(892142420833, --[[ModItemInventoryItemCompositeDef JazzArmor_TwaronFull AdditionalHint]] "Модульный бронежилет. Штурмовой вариант"),
	Cost = 7000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Neck", "Torso" ),
	Coverage = 95,
	ArmorRating = 16,
	MeleeArmorRating = 25,
	ExplosiveArmorRating = 40,
	CamouflagePercent = 1,
	CanHoldPlate = true,
	Weight = 4,
	SuppressionProtection = 25,
}

