UndefineClass('FlakLeggings_Kompositum')
DefineClass.FlakLeggings_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/flak_leggings",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(700961137268, --[[ModItemInventoryItemCompositeDef FlakLeggings_Kompositum DisplayName]] "Kompositum Flak Leggings"),
	DisplayNamePlural = T(476332394039, --[[ModItemInventoryItemCompositeDef FlakLeggings_Kompositum DisplayNamePlural]] "Kompositum Flak Leggings"),
	AdditionalHint = T(981675853444, --[[ModItemInventoryItemCompositeDef FlakLeggings_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещены с композитумом-58"),
	Cost = 800,
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

