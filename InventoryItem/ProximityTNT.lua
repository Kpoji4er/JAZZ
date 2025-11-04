UndefineClass('ProximityTNT')
DefineClass.ProximityTNT = {
	__parents = { "ThrowableTrapItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ThrowableTrapItem",
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/proximity_tnt",
	ItemType = "Grenade",
	DisplayName = T(199359640589, "Бесконтактный динамит"),
	DisplayNamePlural = T(534936218786, "Бесконтактный динамит"),
	AdditionalHint = T(380950777375, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается, когда враг подходит к заряду на близкое расстояние\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая вероятность неудачи"),
	UnitStat = "Explosives",
	Cost = 600,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Grenade",
	MaxStacks = 2,
	MinMishapChance = 2,
	MaxMishapChance = 30,
	MaxMishapRange = 6,
	AttackAP = 4000,
	BaseRange = 3,
	CanBounce = false,
	Noise = 30,
	Entity = "Explosive_TNT",
	ActionIcon = "UI/Icons/Hud/throw_proximity_explosive",
	TriggerType = "Proximity",
}

