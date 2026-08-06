UndefineClass('TNT')
DefineClass.TNT = {
	__parents = { "ExplosiveSubstance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstance",
	Repairable = false,
	Icon = "UI/Icons/Items/tnt",
	DisplayName = T(617720797508, --[[ModItemInventoryItemCompositeDef TNT DisplayName]] "TNT"),
	DisplayNamePlural = T(598565600988, --[[ModItemInventoryItemCompositeDef TNT DisplayNamePlural]] "TNT"),
	Description = T(822428525866, --[[ModItemInventoryItemCompositeDef TNT Description]] "The go-to tool of railroad builders and Wild West moustache villains, the TNT is easy to find, use and abuse."),
	AdditionalHint = T(634006657340, --[[ModItemInventoryItemCompositeDef TNT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Добавьте взрыватель, чтобы создать взрывчатку\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный радиус взрыва"),
	UnitStat = "Explosives",
	Cost = 150,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 50,
	MaxStock = 5,
	CategoryPair = "Components",
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"KnockDown",
	},
	AreaOfEffect = 5,
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 60,
	AreaObjDamageMod = 500,
	PenetrationClass = 1,
	DeathType = "BlowUp",
	BaseDamage = 120,
	Noise = 30,
}

