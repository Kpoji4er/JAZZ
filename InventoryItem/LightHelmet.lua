UndefineClass('LightHelmet')
DefineClass.LightHelmet = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 32,
	Icon = "UI/Icons/Items/light_helmet",
	DisplayName = T(513659519711, --[[ModItemInventoryItemCompositeDef LightHelmet DisplayName]] "Light Helmet"),
	DisplayNamePlural = T(319467048749, --[[ModItemInventoryItemCompositeDef LightHelmet DisplayNamePlural]] "Light Helmets"),
	RestockWeight = 35,
	CategoryPair = "Light",
	Slot = "Head",
	PenetrationClass = 2,
	AdditionalReduction = 40,
	ProtectedBodyParts = set( "Head" ),
}

