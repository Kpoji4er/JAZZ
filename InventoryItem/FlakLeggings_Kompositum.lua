UndefineClass('FlakLeggings_Kompositum')
DefineClass.FlakLeggings_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 16,
	Icon = "UI/Icons/Items/flak_leggings",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(670921772841, "Противооскол. поножи с композитумом"),
	DisplayNamePlural = T(695923433132, "Противооскол. поножи с композитумом"),
	AdditionalHint = T(981675853444, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещены с композитумом-58"),
	Cost = 800,
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Legs",
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 60,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

