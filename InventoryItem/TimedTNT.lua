UndefineClass('TimedTNT')
DefineClass.TimedTNT = {
	__parents = { "ThrowableTrapItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ThrowableTrapItem",
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/timed_tnt",
	ItemType = "Grenade",
	DisplayName = T(172654624200, --[[ModItemInventoryItemCompositeDef TimedTNT DisplayName]] "Timed TNT"),
	DisplayNamePlural = T(452046444287, --[[ModItemInventoryItemCompositeDef TimedTNT DisplayNamePlural]] "Timed TNT"),
	AdditionalHint = T(714276674088, --[[ModItemInventoryItemCompositeDef TimedTNT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Взрывается через 1 ход (или 5 секунд не в бою)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая вероятность неудачи"),
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
	ActionIcon = "UI/Icons/Hud/throw_timed_explosives",
	TriggerType = "Timed",
}

