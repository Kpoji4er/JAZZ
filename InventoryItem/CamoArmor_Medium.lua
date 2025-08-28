UndefineClass('CamoArmor_Medium')
DefineClass.CamoArmor_Medium = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/camo_armor_medium",
	DisplayName = T(129566548767, "Ср. камуфляжная броня"),
	DisplayNamePlural = T(914089961047, "Ср. камуфляжная броня"),
	AdditionalHint = T(841350375386, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усложняет обнаружение противником\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Против камуфлированных целей прицеливание работает хуже\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нельзя совмещать с обивкой или керамическими пластинами"),
	Cost = 9000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	PenetrationClass = 3,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Camouflage = true,
}

