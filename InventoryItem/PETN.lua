UndefineClass('PETN')
DefineClass.PETN = {
	__parents = { "ExplosiveSubstance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstance",
	Repairable = false,
	Icon = "UI/Icons/Items/petn",
	DisplayName = T(869513898364, "ТЭН"),
	DisplayNamePlural = T(186780614723, "ТЭНы"),
	Description = T(269747748923, "Мощная пластическая взрывчатка, используется как в подрывных зарядах, так и в военных целях."),
	AdditionalHint = T(948394818720, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Добавьте взрыватель, чтобы создать взрывчатку"),
	UnitStat = "Explosives",
	Cost = 200,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 35,
	CategoryPair = "Components",
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"KnockDown",
	},
	AreaOfEffect = 4,
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 60,
	AreaObjDamageMod = 500,
	PenetrationClass = 1,
	DeathType = "BlowUp",
	BaseDamage = 100,
}

