UndefineClass('LightHelmet')
DefineClass.LightHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 32,
	Icon = "UI/Icons/Items/light_helmet",
	DisplayName = T(524136732156, --[[ModItemInventoryItemCompositeDef LightHelmet DisplayName]] "Легкий шлем"),
	DisplayNamePlural = T(362915776105, --[[ModItemInventoryItemCompositeDef LightHelmet DisplayNamePlural]] "Легкие шлемы"),
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Head",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Head" ),
}

