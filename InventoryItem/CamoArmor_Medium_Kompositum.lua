UndefineClass('CamoArmor_Medium_Kompositum')
DefineClass.CamoArmor_Medium_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/camo_armor_medium",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(480082810804, "Ср. камуфляжная броня с композитумом"),
	DisplayNamePlural = T(379301758740, "Ср. камуфляжная броня с композитумом"),
	AdditionalHint = T(778372553788, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усложняет обнаружение противником\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Против камуфлированных целей прицеливание работает хуже\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещена с композитумом-58"),
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

