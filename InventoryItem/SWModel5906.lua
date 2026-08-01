UndefineClass('SWModel5906')
DefineClass.SWModel5906 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 4,
	Reliability = 75,
	Icon = "Mod/e6L4ECj/WeaponIcons/SW5906.png",
	DisplayName = T(890000000001152, --[[ModItemInventoryItemCompositeDef SWModel5906 DisplayName]] "S&W Model 5906"),
	DisplayNamePlural = T(890000000001292, --[[ModItemInventoryItemCompositeDef SWModel5906 DisplayNamePlural]] "S&W Model 5906"),
	Description = T(890000000000013, --[[ModItemInventoryItemCompositeDef SWModel5906 Description]] "Третье поколение пистолетов Смита и Вессона, с рамкой и затвором полностью из нержавеющей стали. Как и другие пистолеты этой линейки - представляет собой развитие системы 1911. Имеет увеличенный магазин на 15 патронов 9 мм Люгер."),
	AdditionalHint = T(890000000000611, --[[ModItemInventoryItemCompositeDef SWModel5906 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Конкуретный"),
	UnitStat = "Marksmanship",
	Cost = 1250,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 24,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	CritChanceScaled = 35,
	MagazineSize = 16,
	WeaponRange = 19,
	OverwatchAngle = 5400,
	Noise = 22,
	Entity = "SWModel5906",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagLarge",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'CanBeEmpty', true,
			'AvailableComponents', {
								"JAZZ_ImprovisedSuppressor",
								"JAZZ_Suppressor",
							},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"JAZZ_Freeswap",
			},
			'DefaultComponent', "JAZZ_Freeswap",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"MobileShot",
		"JAZZ_Mozambique",
		"JAZZ_DoubleTap",
	},
	ShootAP = 3000,
	ReloadAP = 4000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 6,
	Grouping = 74,
	BaseJamChance = -20,
}

