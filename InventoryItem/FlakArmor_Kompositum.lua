UndefineClass('FlakArmor_Kompositum')
DefineClass.FlakArmor_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/flak_armor",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(977366157430, --[[ModItemInventoryItemCompositeDef FlakArmor_Kompositum DisplayName]] "Kompositum Flak Armor"),
	DisplayNamePlural = T(210530158086, --[[ModItemInventoryItemCompositeDef FlakArmor_Kompositum DisplayNamePlural]] "Kompositum Flak Armors"),
	AdditionalHint = T(470237496402, --[[ModItemInventoryItemCompositeDef FlakArmor_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещена с композитумом-58"),
	Cost = 1200,
	MaxStock = 2,
	RestockWeight = 75,
	CategoryPair = "Light",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

