UndefineClass('HeavyArmorHelmet')
DefineClass.HeavyArmorHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_helmet",
	DisplayName = T(674090196987, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet DisplayName]] "Heavy Armor Helmet"),
	DisplayNamePlural = T(934219027606, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet DisplayNamePlural]] "Heavy Armor Helmets"),
	AdditionalHint = T(852703817426, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 5000,
	Tier = 3,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	Slot = "Head",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Head" ),
}

