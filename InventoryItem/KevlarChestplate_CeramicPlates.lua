UndefineClass('KevlarChestplate_CeramicPlates')
DefineClass.KevlarChestplate_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_vest",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(960351847723, "Кевларовый жилет"),
	DisplayNamePlural = T(638224036453, "Кевларовые жилеты"),
	AdditionalHint = T(926317299683, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами) \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий"),
	Cost = 2800,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	PenetrationClass = 3,
	DamageReduction = 40,
	AdditionalReduction = 90,
	ProtectedBodyParts = set( "Torso" ),
}

