UndefineClass('HeavyArmorChestplate_CeramicPlates')
DefineClass.HeavyArmorChestplate_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_vest",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(753691133305, "Тяжелый жилет"),
	DisplayNamePlural = T(738672896289, "Тяжелые жилеты"),
	AdditionalHint = T(331960463954, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 7000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	PenetrationClass = 4,
	DamageReduction = 40,
	AdditionalReduction = 90,
	ProtectedBodyParts = set( "Torso" ),
}

