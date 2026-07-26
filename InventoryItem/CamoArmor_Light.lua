UndefineClass('CamoArmor_Light')
DefineClass.CamoArmor_Light = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/camo_armor_light",
	DisplayName = T(623928157955, --[[ModItemInventoryItemCompositeDef CamoArmor_Light DisplayName]] "Light Camo Armor"),
	DisplayNamePlural = T(728180263372, --[[ModItemInventoryItemCompositeDef CamoArmor_Light DisplayNamePlural]] "Light Camo Armors"),
	AdditionalHint = T(492059399247, --[[ModItemInventoryItemCompositeDef CamoArmor_Light AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Усложняет обнаружение противником\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Против камуфлированных целей прицеливание работает хуже\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нельзя совмещать с обивкой или керамическими пластинами"),
	Cost = 4500,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Light",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
	Camouflage = true,
}

