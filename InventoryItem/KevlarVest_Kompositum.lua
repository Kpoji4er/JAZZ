UndefineClass('KevlarVest_Kompositum')
DefineClass.KevlarVest_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/kevlar_armor",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(224548841891, --[[ModItemInventoryItemCompositeDef KevlarVest_Kompositum DisplayName]] "Kompositum Kevlar Armor"),
	DisplayNamePlural = T(278978522121, --[[ModItemInventoryItemCompositeDef KevlarVest_Kompositum DisplayNamePlural]] "Kompositum Kevlar Armors"),
	AdditionalHint = T(455311699523, --[[ModItemInventoryItemCompositeDef KevlarVest_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	Cost = 2800,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 50,
	CategoryPair = "Medium",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

