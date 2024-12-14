UndefineClass('SVT40')
DefineClass.SVT40 = {
	__parents = { "SniperRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1+",
	object_class = "SniperRifle",
	ScrapParts = 8,
	Icon = "Mod/e6L4ECj/WeaponIcons/SVT40.png",
	DisplayName = T(514199755077, --[[ModItemInventoryItemCompositeDef SVT40 DisplayName]] "СВТ-40"),
	DisplayNamePlural = T(625382131145, --[[ModItemInventoryItemCompositeDef SVT40 DisplayNamePlural]] "СВТ-40"),
	Description = T(683949352379, --[[ModItemInventoryItemCompositeDef SVT40 Description]] '"Светлана" Федоровна Токарева, прошу любить и жаловать. Самозарядная винтовка СССР периода начала ВОВ. "Света" оказалась дамой очень капризной и требовательной к уходу, так что с работой в боевых частях Красной армии у нее не заладилось, а вот более подготовленные морские пехотинцы "Светку" использовали с удовольствием вплоть до самого конца войны.'),
	AdditionalHint = T(561907040232, --[[ModItemInventoryItemCompositeDef SVT40 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий урон"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 5000,
	CategoryPair = "Rifles",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_762x54R",
	Damage = 38,
	AimAccuracy = 30,
	CritChanceScaled = 40,
	MagazineSize = 10,
	WeaponRange = 64,
	OverwatchAngle = 900,
	Noise = 85,
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
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	ModifyRightHandGrip = true,
	AvailableAttacks = {
		"SingleShot",
		"CancelShot",
	},
	ShootAP = 5000,
	ReloadAP = 7000,
	BurstShots = 1,
	AutoShots = 1,
	Handling = 30,
	BulletDropRange = 24,
	Grouping = 255,
}

