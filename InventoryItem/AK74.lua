UndefineClass('AK74')
DefineClass.AK74 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "AssaultRifle",
	ScrapParts = 10,
	RepairCost = 10,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/AK74.png",
	DisplayName = T(489350715496, --[[ModItemInventoryItemCompositeDef AK74 DisplayName]] "АК74"),
	DisplayNamePlural = T(261108237192, --[[ModItemInventoryItemCompositeDef AK74 DisplayNamePlural]] "АК74"),
	Description = T(790591991065, --[[ModItemInventoryItemCompositeDef AK74 Description]] "The Soviets revisited their emblematic design around 1974 and this beauty was born. It has sprouted many variations but keeps the long stroke gas piston system of the original design."),
	AdditionalHint = T(216627067101, --[[ModItemInventoryItemCompositeDef AK74 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Слабая отдача \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Быстро стреляет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Лучшее оружие для вашей войны."),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 8500,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 70,
	CategoryPair = "AssaultRifles",
	Caliber = "JAZZ_Caliber_545",
	Damage = 26,
	ObjDamageMod = 45,
	AimAccuracy = 12,
	CritChanceScaled = 20,
	MagazineSize = 30,
	WeaponRange = 48,
	OverwatchAngle = 1320,
	Noise = 49,
	HandSlot = "TwoHanded",
	Entity = "AK74",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"JAZZ_StockNormal",
				"JAZZ_StockLightFolded",
				"JAZZ_StockLightUnFolded",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Handguard",
			},
			'DefaultComponent', "JAZZ_Handguard",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagQuick_AK",
				"JAZZ_MagLarge_30_45",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Under",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_GP25",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Scope_PSO",
				"JAZZ_Reflex_Cobra",
				"JAZZ_Reflex_PKAS",
				"JAZZ_CombatScope_1P29",
				"JAZZ_NightScope_NSPU",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"JAZZ_ManeuverAR",
		"JAZZ_ControllableBurst",
		"JAZZ_LargeAutoFire",
	},
	ShootAP = 5000,
	ReloadAP = 6000,
	WeaponMass = 35,
	CyclicRPM = 650,
	WeaponSizeClass = "Rifle",
	BurstLimiter = 0,
	BurstShots = 3,
	Recoil = 15,
	AutoShots = 6,

	CloseRange = 8,

	CloseRangeFactor = 85,
	BulletDropRange = 16,
	Grouping = 56,
	BaseJamChance = -50,
	WeaponResource = 9800,
}

