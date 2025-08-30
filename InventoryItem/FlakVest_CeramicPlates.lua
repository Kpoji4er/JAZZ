UndefineClass('FlakVest_CeramicPlates')
DefineClass.FlakVest_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_vest",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(688366129736, --[[ModItemInventoryItemCompositeDef FlakVest_CeramicPlates DisplayName]] "Противооскол. жилет"),
	DisplayNamePlural = T(690006158155, --[[ModItemInventoryItemCompositeDef FlakVest_CeramicPlates DisplayNamePlural]] "Противооскол. жилеты"),
	AdditionalHint = T(907738433164, --[[ModItemInventoryItemCompositeDef FlakVest_CeramicPlates AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами) \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий"),
	Cost = 1600,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	PenetrationClass = 2,
	DamageReduction = 40,
	AdditionalReduction = 70,
	ProtectedBodyParts = set( "Torso" ),
}

