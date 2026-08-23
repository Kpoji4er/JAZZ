UndefineClass('Unarmed')
DefineClass.Unarmed = {
	__parents = { "UnarmedWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "UnarmedWeapon",
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Weapons/Fist",
	DisplayName = T(738226804609, --[[ModItemInventoryItemCompositeDef Unarmed DisplayName]] "Unarmed"),
	DisplayNamePlural = T(262841837142, --[[ModItemInventoryItemCompositeDef Unarmed DisplayNamePlural]] "Unarmed"),
	AdditionalHint = T(694647651138, --[[ModItemInventoryItemCompositeDef Unarmed AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Небольшой урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный эффект от силы\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Очень высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Значительно увеличенная эффективность прицеливания"),
	UnitStat = "Strength",
	Cost = 0,
	RestockWeight = 0,
	CategoryPair = "MeleeWeapons",
	BaseChanceToHit = 100,
	CritChanceScaled = 50,
	BaseDamage = 5,
	AimAccuracy = 25,
	PenetrationClass = 4,
	DamageMultiplier = 300,
	WeaponRange = 0,
	IsUnarmed = true,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	NeckAttackType = "choke",
}

