UndefineClass('HeavyArmorChestplate_Kompositum')
DefineClass.HeavyArmorChestplate_Kompositum = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 12,
	Icon = "UI/Icons/Items/heavy_vest",
	SubIcon = "UI/Icons/Items/kompositum58.png",
	DisplayName = T(949961773018, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate_Kompositum DisplayName]] "Kompositum Heavy Vest"),
	DisplayNamePlural = T(576829632928, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate_Kompositum DisplayNamePlural]] "Kompositum Heavy Vests"),
	AdditionalHint = T(750816289329, --[[ModItemInventoryItemCompositeDef HeavyArmorChestplate_Kompositum AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Совмещено с композитумом-58"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 4300,
	Tier = 3,
	RestockWeight = 50,
	CategoryPair = "Heavy",
	PenetrationClass = 5,
	DamageReduction = 40,
	AdditionalReduction = 85,
	ProtectedBodyParts = set( "Torso" ),
}

