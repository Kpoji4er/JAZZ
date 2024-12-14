UndefineClass('HeavyArmorTorso_Kompositum')
DefineClass.HeavyArmorTorso_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/heavy_armor",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(615129134579, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_Kompositum DisplayName]] "Тяжелая броня с композитумом"),
	DisplayNamePlural = T(126914512957, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_Kompositum DisplayNamePlural]] "Тяжелая броня с композитумом"),
	AdditionalHint = T(347531284201, --[[ModItemInventoryItemCompositeDef HeavyArmorTorso_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещено с композитумом-58"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 5500,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 50,
	CategoryPair = "Heavy",
	PenetrationClass = 5,
	DamageReduction = 35,
	AdditionalReduction = 85,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

