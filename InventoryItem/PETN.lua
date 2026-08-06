UndefineClass('PETN')
DefineClass.PETN = {
	__parents = { "ExplosiveSubstance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "ExplosiveSubstance",
	Repairable = false,
	Icon = "UI/Icons/Items/petn",
	DisplayName = T(840692162750, --[[ModItemInventoryItemCompositeDef PETN DisplayName]] "PETN"),
	DisplayNamePlural = T(916343361606, --[[ModItemInventoryItemCompositeDef PETN DisplayNamePlural]] "PETN"),
	Description = T(186864246396, --[[ModItemInventoryItemCompositeDef PETN Description]] "A powerful plastic explosive substance used in major demolition and military high-grade explosives."),
	AdditionalHint = T(948394818720, --[[ModItemInventoryItemCompositeDef PETN AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Добавьте взрыватель, чтобы создать взрывчатку"),
	UnitStat = "Explosives",
	Cost = 450,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 25,
	MaxStock = 3,
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

