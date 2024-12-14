UndefineClass('PierreMachete')
DefineClass.PierreMachete = {
	__parents = { "MacheteWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MacheteWeapon",
	ScrapParts = 2,
	Reliability = 50,
	Icon = "UI/Icons/Weapons/pierre_machete",
	DisplayName = T(856581366127, --[[ModItemInventoryItemCompositeDef PierreMachete DisplayName]] "«Гордость Легиона»"),
	DisplayNamePlural = T(382530254567, --[[ModItemInventoryItemCompositeDef PierreMachete DisplayNamePlural]] "«Гордость Легиона»"),
	AdditionalHint = T(149238847516, --[[ModItemInventoryItemCompositeDef PierreMachete AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный доп. урон от силы\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки"),
	LargeItem = 1,
	UnitStat = "Dexterity",
	Cost = 150,
	locked = true,
	RestockWeight = 0,
	BaseChanceToHit = 100,
	CritChanceScaled = 30,
	BaseDamage = 16,
	AimAccuracy = 15,
	PenetrationClass = 4,
	DamageMultiplier = 350,
	WeaponRange = 0,
	Charge = true,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	NeckAttackType = "lethal",
	Entity = "Weapon_Machete_01",
	HolsterSlot = "Shoulder",
}

