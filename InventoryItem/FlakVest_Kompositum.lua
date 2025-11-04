UndefineClass('FlakVest_Kompositum')
DefineClass.FlakVest_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/flak_vest",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(880388662664, --[[ModItemInventoryItemCompositeDef FlakVest_Kompositum DisplayName]] "Противооскол. жилет с композитумом"),
	DisplayNamePlural = T(402243986328, --[[ModItemInventoryItemCompositeDef FlakVest_Kompositum DisplayNamePlural]] "Противооскол. жилеты с композитумом"),
	AdditionalHint = T(488626459232, --[[ModItemInventoryItemCompositeDef FlakVest_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	Cost = 800,
	RestockWeight = 75,
	CategoryPair = "Light",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Torso" ),
}

