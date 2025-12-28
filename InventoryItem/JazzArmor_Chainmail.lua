UndefineClass('JazzArmor_Chainmail')
DefineClass.JazzArmor_Chainmail = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Class1 M T1",
	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 60,
	Icon = "Mod/e6L4ECj/ArmorIcons/Chainmail.png",
	DisplayName = T(255285870071, "Самодельная кольчуга"),
	DisplayNamePlural = T(796729854508, "Самодельные кольчуги"),
	Description = T(866133024791, "В отсуствие фабричных средств защиты, Легион Патриотов Гранд-Чиена вынужден прибегать к кустарному производству их из подручных материалов. Ржавая кольчуга из проволоки против холодного оружия и противоосколочные резиновые пластины из шин. Страшно подумать, что сумрачный гений дизайнера этой брони был бы способен произвести в условиях большего изобилия ресурсов."),
	AdditionalHint = T(659912789786, "Самодельная кольчуга из железа из шин. Разработана и введена в эксплуатацию Легионом"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Arms", "Groin", "Neck", "Torso" ),
	ArmorRating = 5,
	MeleeArmorRating = 100,
	ExplosiveArmorRating = 5,
	CamouflagePercent = -10,
	Weight = 3,
	ArmorResource = 200,
	Repairability = 95,
}

