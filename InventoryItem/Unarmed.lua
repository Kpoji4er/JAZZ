UndefineClass('Unarmed')
DefineClass.Unarmed = {
	__parents = { "UnarmedWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "UnarmedWeapon",
	Repairable = false,
	Reliability = 100,
	Icon = "UI/Icons/Weapons/Fist",
	DisplayName = T(157754371372, --[[ModItemInventoryItemCompositeDef Unarmed DisplayName]] "Без оружия"),
	DisplayNamePlural = T(841542978000, --[[ModItemInventoryItemCompositeDef Unarmed DisplayNamePlural]] "Без оружия"),
	AdditionalHint = T(694647651138, --[[ModItemInventoryItemCompositeDef Unarmed AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Небольшой урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный эффект от силы\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Очень высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Значительно увеличенная эффективность прицеливания"),
	UnitStat = "Dexterity",
	Cost = 0,
	RestockWeight = 0,
	CategoryPair = "MeleeWeapons",
	BaseChanceToHit = 100,
	CritChanceScaled = 50,
	BaseDamage = 5,
	AimAccuracy = 25,
	PenetrationClass = 4,
	DamageMultiplier = 600,
	WeaponRange = 0,
	IsUnarmed = true,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	NeckAttackType = "choke",
}

