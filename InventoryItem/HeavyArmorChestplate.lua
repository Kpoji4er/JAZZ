UndefineClass('HeavyArmorChestplate')
DefineClass.HeavyArmorChestplate = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_vest",
	DisplayName = T(410197513169, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate DisplayName]] "Heavy Vest"),
	DisplayNamePlural = T(458596493579, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate DisplayNamePlural]] "Heavy Vests"),
	AdditionalHint = T(221146537482, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 4300,
	Tier = 3,
	RestockWeight = 50,
	CategoryPair = "Heavy",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Torso" ),
}

