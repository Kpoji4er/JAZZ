UndefineClass('EndlessKnives')
DefineClass.EndlessKnives = {
	__parents = { "MeleeWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MeleeWeapon",
	Reliability = 50,
	Icon = "UI/Icons/Weapons/EndlessKnives",
	DisplayName = T(996476550790, --[[ModItemInventoryItemCompositeDef EndlessKnives DisplayName]] "Endless Knives"),
	DisplayNamePlural = T(262652558760, --[[ModItemInventoryItemCompositeDef EndlessKnives DisplayNamePlural]] "Endless Knives"),
	Description = T(932962724262, --[[ModItemInventoryItemCompositeDef EndlessKnives Description]] "Блад лично выбирал и точил каждый режик и ножик из своего набора. Вот тем, большим, можно рубить хворост, вот этим, широким - делать вырезку. А вот этот для скальпов. И этот. И вон тот."),
	AdditionalHint = T(873120430532, --[[ModItemInventoryItemCompositeDef EndlessKnives AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Всегда под рукой!\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	UnitStat = "Dexterity",
	Cost = 150,
	locked = true,
	RestockWeight = 0,
	BaseChanceToHit = 100,
	CritChance = 5,
	CritChanceScaled = 20,
	BaseDamage = 22,
	AimAccuracy = 20,
	PenetrationClass = 4,
	DamageMultiplier = 100,
	CanThrow = true,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	Entity = "Weapon_FC_AMZ_Knife_01",
	HolsterSlot = "Leg",
}

