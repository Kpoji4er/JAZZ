UndefineClass('TNT')
DefineClass.TNT = {
	__parents = { "ExplosiveSubstance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstance",
	Repairable = false,
	Icon = "UI/Icons/Items/tnt",
	DisplayName = T(676828264605, --[[ModItemInventoryItemCompositeDef TNT DisplayName]] "Динамит"),
	DisplayNamePlural = T(415965676052, --[[ModItemInventoryItemCompositeDef TNT DisplayNamePlural]] "Динамит"),
	Description = T(789251709752, --[[ModItemInventoryItemCompositeDef TNT Description]] "Излюбленная палочка-выручалочка американских железнодорожных рабочих и усатых злодеев. С такой шашкой любой выйдет в дамки."),
	AdditionalHint = T(634006657340, --[[ModItemInventoryItemCompositeDef TNT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Добавьте взрыватель, чтобы создать взрывчатку\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный радиус взрыва"),
	UnitStat = "Explosives",
	Cost = 100,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 60,
	CategoryPair = "Components",
	CenterObjDamageMod = 300,
	CenterAppliedEffects = {
		"KnockDown",
	},
	AreaOfEffect = 5,
	CenterAreaOfEffect = 2,
	AreaUnitDamageMod = 60,
	AreaObjDamageMod = 150,
	PenetrationClass = 1,
	DeathType = "BlowUp",
	BaseDamage = 120,
	Noise = 30,
}

