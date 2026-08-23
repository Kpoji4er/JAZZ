UndefineClass('PierreMachete')
DefineClass.PierreMachete = {
	__parents = { "MacheteWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MacheteWeapon",
	ScrapParts = 2,
	Reliability = 50,
	Icon = "UI/Icons/Weapons/pierre_machete",
	DisplayName = T(646705990009, --[[ModItemInventoryItemCompositeDef PierreMachete DisplayName]] "Legion's Pride"),
	DisplayNamePlural = T(624754374783, --[[ModItemInventoryItemCompositeDef PierreMachete DisplayNamePlural]] "Legion's Pride"),
	Description = T(337230371768, --[[ModItemInventoryItemCompositeDef PierreMachete Description]] '"Гордость Легиона". Пафосное имя, выданное, в общем-то, обычной рядовой железяке, рубящей тростник. Это у Пьера возрастное, пройдет.'),
	AdditionalHint = T(149238847516, --[[ModItemInventoryItemCompositeDef PierreMachete AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный доп. урон от силы\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки"),
	LargeItem = 1,
	UnitStat = "Strength",
	Cost = 150,
	RestockWeight = 0,
	BaseChanceToHit = 100,
	CritChanceScaled = 30,
	BaseDamage = 16,
	AimAccuracy = 15,
	PenetrationClass = 4,
	DamageMultiplier = 250,
	WeaponRange = 0,
	Charge = true,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	NeckAttackType = "lethal",
	Entity = "Weapon_Machete_01",
	HolsterSlot = "Shoulder",
}

