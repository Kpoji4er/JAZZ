UndefineClass('HeavyArmorTorso_WeavePadding')
DefineClass.HeavyArmorTorso_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 14,
	Icon = "UI/Icons/Items/heavy_armor",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(947371172255, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_WeavePadding DisplayName]] "Heavy Armor"),
	DisplayNamePlural = T(634699187749, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_WeavePadding DisplayNamePlural]] "Heavy Armors"),
	AdditionalHint = T(190771851393, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 10000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	PenetrationClass = 4,
	DamageReduction = 30,
	AdditionalReduction = 50,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

