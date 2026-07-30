UndefineClass('RemoteTNT')
DefineClass.RemoteTNT = {
	__parents = { "ThrowableTrapItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ThrowableTrapItem",
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Items/remote_tnt",
	ItemType = "Grenade",
	DisplayName = T(814310721881, --[[ModItemInventoryItemCompositeDef RemoteTNT DisplayName]] "Remote TNT"),
	DisplayNamePlural = T(850557903938, --[[ModItemInventoryItemCompositeDef RemoteTNT DisplayNamePlural]] "Remote TNT"),
	AdditionalHint = T(436102360957, --[[ModItemInventoryItemCompositeDef RemoteTNT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Заряд подрывается с помощью пульта ДУ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая вероятность неудачи"),
	UnitStat = "Explosives",
	Cost = 600,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	CategoryPair = "Grenade",
	MaxStacks = 2,
	MinMishapChance = 2,
	MaxMishapChance = 50,
	MaxMishapRange = 6,
	AttackAP = 4000,
	BaseRange = 3,
	CanBounce = false,
	Noise = 30,
	Entity = "Explosive_TNT",
	ActionIcon = "UI/Icons/Hud/throw_remote_explosive",
	TriggerType = "Remote",
}

