UndefineClass('HeavyArmorHelmet_WeavePadding')
DefineClass.HeavyArmorHelmet_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 14,
	Icon = "UI/Icons/Items/heavy_helmet",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(239964731641, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet_WeavePadding DisplayName]] "Heavy Armor Helmet"),
	DisplayNamePlural = T(115190536445, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet_WeavePadding DisplayNamePlural]] "Heavy Armor Helmets"),
	AdditionalHint = T(353912792254, --[[ModItemInventoryItemCompositeDef HeavyArmorHelmet_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 10000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	Slot = "Head",
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Head" ),
}

