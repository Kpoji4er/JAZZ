UndefineClass('HeavyArmorTorso_CeramicPlates')
DefineClass.HeavyArmorTorso_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/heavy_armor",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(273015700050, "Тяжелая броня"),
	DisplayNamePlural = T(316544463324, "Тяжелая броня"),
	AdditionalHint = T(603800970086, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Громоздкое (нет бесплатного перемещения)"),
	Cumbersome = 1,
	Valuable = 1,
	Cost = 10000,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Heavy",
	CanAppearStandard = false,
	PenetrationClass = 4,
	DamageReduction = 40,
	AdditionalReduction = 90,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

