UndefineClass('BlackPowder')
DefineClass.BlackPowder = {
	__parents = { "ExplosiveSubstanceSquadBagItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstanceSquadBagItem",
	Repairable = false,
	Icon = "UI/Icons/Items/black_powder",
	DisplayName = T(253597811751, "Порох"),
	DisplayNamePlural = T(321461865710, "Порох"),
	AdditionalHint = T(565959045541, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется в ходе операций «Изготовление боеприпасов» и «Изготовление взрывчатки»"),
	UnitStat = "Explosives",
	Cost = 200,
	CanAppearInShop = true,
	MaxStock = 10,
	CategoryPair = "Components",
	ShopStackSize = 5,
	CenterObjDamageMod = 50,
	CenterAppliedEffects = {
		"Bleeding",
	},
	AreaOfEffect = 4,
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 10,
	AreaObjDamageMod = 10,
	AreaAppliedEffects = {
		"Bleeding",
		"Bleeding",
	},
	PenetrationClass = 1,
	BurnGround = false,
	DeathType = "BlowUp",
	BaseDamage = 60,
	Noise = 100,
}

