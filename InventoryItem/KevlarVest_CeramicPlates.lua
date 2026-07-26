UndefineClass('KevlarVest_CeramicPlates')
DefineClass.KevlarVest_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 28,
	Icon = "UI/Icons/Items/kevlar_armor",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(982997486407, --[[ModItemInventoryItemCompositeDef KevlarVest_CeramicPlates DisplayName]] "Kevlar Armor"),
	DisplayNamePlural = T(430963369197, --[[ModItemInventoryItemCompositeDef KevlarVest_CeramicPlates DisplayNamePlural]] "Kevlar Armors"),
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

