UndefineClass('KevlarChestplate_WeavePadding')
DefineClass.KevlarChestplate_WeavePadding = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 4,
	Degradation = 20,
	Icon = "UI/Icons/Items/kevlar_vest",
	SubIcon = "UI/Icons/Items/padded",
	DisplayName = T(672086153382, --[[ModItemInventoryItemCompositeDef KevlarChestplate_WeavePadding DisplayName]] "Kevlar Vest"),
	DisplayNamePlural = T(534763739172, --[[ModItemInventoryItemCompositeDef KevlarChestplate_WeavePadding DisplayNamePlural]] "Kevlar Vests"),
	AdditionalHint = T(980764623412, --[[ModItemInventoryItemCompositeDef KevlarChestplate_WeavePadding AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшение урона (улучшено обивкой)"),
	Cost = 2800,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "Medium",
	CanAppearStandard = false,
	PenetrationClass = 3,
	DamageReduction = 20,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Torso" ),
}

