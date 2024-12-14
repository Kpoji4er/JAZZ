UndefineClass('KevlarVest_CeramicPlates')
DefineClass.KevlarVest_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_armor",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(196362455670, --[[ModItemInventoryItemCompositeDef KevlarVest_CeramicPlates DisplayName]] "Кевларовая броня"),
	DisplayNamePlural = T(819102510854, --[[ModItemInventoryItemCompositeDef KevlarVest_CeramicPlates DisplayNamePlural]] "Кевларовая броня"),
	AdditionalHint = T(904920821332, --[[ModItemInventoryItemCompositeDef KevlarVest_CeramicPlates AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами) \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий"),
	Cost = 5000,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	PenetrationClass = 3,
	AdditionalReduction = 90,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

