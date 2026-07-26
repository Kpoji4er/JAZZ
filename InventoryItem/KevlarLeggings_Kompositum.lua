UndefineClass('KevlarLeggings_Kompositum')
DefineClass.KevlarLeggings_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/kevlar_leggings",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(157610373366, --[[ModItemInventoryItemCompositeDef KevlarLeggings_Kompositum DisplayName]] "Kompositum Kevlar Leggings"),
	DisplayNamePlural = T(226479029140, --[[ModItemInventoryItemCompositeDef KevlarLeggings_Kompositum DisplayNamePlural]] "Kompositum Kevlar Leggings"),
	AdditionalHint = T(458558922661, --[[ModItemInventoryItemCompositeDef KevlarLeggings_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	Cost = 1400,
	Tier = 2,
	RestockWeight = 25,
	CategoryPair = "Medium",
	Slot = "Legs",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

