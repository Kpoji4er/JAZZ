UndefineClass('CamoArmor_Light_Kompositum')
DefineClass.CamoArmor_Light_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/camo_armor_light",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(925164820871, --[[ModItemInventoryItemCompositeDef CamoArmor_Light_Kompositum DisplayName]] "Лег. камуфляжная броня с композитумом"),
	DisplayNamePlural = T(216023440060, --[[ModItemInventoryItemCompositeDef CamoArmor_Light_Kompositum DisplayNamePlural]] "Лег. камуфляжная броня с композитумом"),
	AdditionalHint = T(940302072624, --[[ModItemInventoryItemCompositeDef CamoArmor_Light_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усложняет обнаружение противником\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Против камуфлированных целей прицеливание работает хуже\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещена с композитумом-58"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Torso" ),
	Camouflage = true,
}

