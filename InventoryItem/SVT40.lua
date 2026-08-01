UndefineClass('SVT40')
DefineClass.SVT40 = {
	__parents = { "BattleRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-3",
	object_class = "BattleRifle",
	ScrapParts = 8,
	RepairCost = 5,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/SVT40.png",
	DisplayName = T(514199755077, --[[ModItemInventoryItemCompositeDef SVT40 DisplayName]] "СВТ-40"),
	DisplayNamePlural = T(625382131145, --[[ModItemInventoryItemCompositeDef SVT40 DisplayNamePlural]] "СВТ-40"),
	Description = T(683949352379, --[[ModItemInventoryItemCompositeDef SVT40 Description]] '"Светлана" Федоровна Токарева, прошу любить и жаловать. Самозарядная винтовка СССР периода начала ВОВ. "Света" оказалась дамой очень капризной и требовательной к уходу, так что с работой в боевых частях Красной армии у нее не заладилось, а вот более подготовленные морские пехотинцы "Светку" использовали с удовольствием вплоть до самого конца войны.'),
	AdditionalHint = T(561907040232, --[[ModItemInventoryItemCompositeDef SVT40 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный Неудобный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 5000,
	CategoryPair = "Rifles",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_762x54R",
	Damage = 38,
	AimAccuracy = 12,
	CritChanceScaled = 30,
	MagazineSize = 10,
	WeaponRange = 64,
	OverwatchAngle = 900,
	Noise = 70,
	HandSlot = "TwoHanded",
	Entity = "SVT_40",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Scope_PU",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	ModifyRightHandGrip = true,
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_Salvo",
	},
	ShootAP = 7000,
	ReloadAP = 7000,
	BurstShots = 1,
	AutoShots = 1,

	CloseRange = 8,

	CloseRangeFactor = 80,
	BulletDropRange = 17,
	Grouping = 38,
	WeaponResource = 2000,
}

