UndefineClass('KevlarChestplate_Kompositum')
DefineClass.KevlarChestplate_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/kevlar_vest",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(409511595554, --[[ModItemInventoryItemCompositeDef KevlarChestplate_Kompositum DisplayName]] "Kompositum Kevlar Vest"),
	DisplayNamePlural = T(723550039441, --[[ModItemInventoryItemCompositeDef KevlarChestplate_Kompositum DisplayNamePlural]] "Kompositum Kevlar Vests"),
	AdditionalHint = T(757854481257, --[[ModItemInventoryItemCompositeDef KevlarChestplate_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещен с композитумом-58"),
	Cost = 1400,
	Tier = 2,
	RestockWeight = 50,
	CategoryPair = "Medium",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 80,
	ProtectedBodyParts = set( "Torso" ),
}

