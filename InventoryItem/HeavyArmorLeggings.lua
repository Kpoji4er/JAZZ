UndefineClass('HeavyArmorLeggings')
DefineClass.HeavyArmorLeggings = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_leggings",
	DisplayName = T(958514093547, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings DisplayName]] "Heavy Armor Leggings"),
	DisplayNamePlural = T(661354623638, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings DisplayNamePlural]] "Heavy Armor Leggings"),
	AdditionalHint = T(562949448257, --[[ModItemInventoryItemCompositeDef HeavyArmorLeggings AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 4300,
	Tier = 3,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	Slot = "Legs",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Groin", "Legs" ),
}

