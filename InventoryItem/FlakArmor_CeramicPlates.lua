UndefineClass('FlakArmor_CeramicPlates')
DefineClass.FlakArmor_CeramicPlates = {
	__parents = { "TransmutedArmor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "TransmutedArmor",
	ScrapParts = 4,
	Degradation = 32,
	Icon = "UI/Icons/Items/flak_armor",
	SubIcon = "UI/Icons/Items/plates",
	DisplayName = T(977066896029, --[[ModItemInventoryItemCompositeDef FlakArmor_CeramicPlates DisplayName]] "Flak Armor"),
	DisplayNamePlural = T(195720969644, --[[ModItemInventoryItemCompositeDef FlakArmor_CeramicPlates DisplayNamePlural]] "Flak Armors"),
	AdditionalHint = T(601923644572, --[[ModItemInventoryItemCompositeDef FlakArmor_CeramicPlates AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено керамическими пластинами) \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Керамические пластины ломаются после <color 124 130 96><RevertConditionCounter></color> попаданий"),
	Cost = 2400,
	MaxStock = 1,
	RestockWeight = 35,
	CategoryPair = "Light",
	CanAppearStandard = false,
	PenetrationClass = 2,
	DamageReduction = 40,
	AdditionalReduction = 70,
	ProtectedBodyParts = set( "Arms", "Torso" ),
}

