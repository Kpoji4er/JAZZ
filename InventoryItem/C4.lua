UndefineClass('C4')
DefineClass.C4 = {
	__parents = { "ExplosiveSubstance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstance",
	Repairable = false,
	Icon = "UI/Icons/Items/c4",
	DisplayName = T(214451267804, "C4"),
	DisplayNamePlural = T(219223135799, "C4"),
	AdditionalHint = T(837276282763, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Добавьте взрыватель, чтобы создать взрывчатку"),
	UnitStat = "Explosives",
	Cost = 200,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 35,
	CategoryPair = "Components",
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"KnockDown",
	},
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 60,
	AreaObjDamageMod = 500,
	PenetrationClass = 1,
	DeathType = "BlowUp",
	BaseDamage = 90,
	Noise = 30,
}

