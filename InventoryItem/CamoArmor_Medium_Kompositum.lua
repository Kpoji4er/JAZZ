UndefineClass('CamoArmor_Medium_Kompositum')
DefineClass.CamoArmor_Medium_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/camo_armor_medium",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(377755048143, --[[ModItemInventoryItemCompositeDef CamoArmor_Medium_Kompositum DisplayName]] "Kompositum Medium Camo Armor"),
	DisplayNamePlural = T(833629193035, --[[ModItemInventoryItemCompositeDef CamoArmor_Medium_Kompositum DisplayNamePlural]] "Kompositum Medium Camo Armors"),
	AdditionalHint = T(778372553788, --[[ModItemInventoryItemCompositeDef CamoArmor_Medium_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усложняет обнаружение противником\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Против камуфлированных целей прицеливание работает хуже\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещена с композитумом-58"),
	Cost = 9000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	PenetrationClass = 4,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Torso" ),
	Camouflage = true,
}

