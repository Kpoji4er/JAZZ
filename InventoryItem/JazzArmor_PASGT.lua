UndefineClass('JazzArmor_PASGT')
DefineClass.JazzArmor_PASGT = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class2 L T2",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "Mod/e6L4ECj/ArmorIcons/PASGT.png",
	DisplayName = T(901708543549, --[[ModItemInventoryItemCompositeDef JazzArmor_PASGT DisplayName]] "Бронежилет PASGT"),
	DisplayNamePlural = T(771481547805, --[[ModItemInventoryItemCompositeDef JazzArmor_PASGT DisplayNamePlural]] "Бронежилеты PASGT"),
	Description = T(760355983161, --[[ModItemInventoryItemCompositeDef JazzArmor_PASGT Description]] 'Дальнейшее развитие бронежилетов серии "Флак". Бронезащита теперь обеспечивается брикетом из 18 слоев кевлара, что усилило защитные свойства относительно в прошлой версии аж в полтора раза.'),
	AdditionalHint = T(487879273384, --[[ModItemInventoryItemCompositeDef JazzArmor_PASGT AdditionalHint]] "Американский бронежилет времен холодной войны"),
	Cost = 4500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 5,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Neck", "Torso" ),
	Coverage = 60,
	ArmorRating = 16,
	MeleeArmorRating = 5,
	ExplosiveArmorRating = 18,
	CamouflagePercent = 8,
	Weight = 3,
	ArmorResource = 280,
	Repairability = 60,
}

