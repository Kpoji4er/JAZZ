UndefineClass('HeavyArmorTorso')
DefineClass.HeavyArmorTorso = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_armor",
	DisplayName = T(269180326225, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso DisplayName]] "Heavy Armor"),
	DisplayNamePlural = T(167239210459, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso DisplayNamePlural]] "Heavy Armors"),
	AdditionalHint = T(219847021710, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 5500,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 50,
	CategoryPair = "Heavy",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

