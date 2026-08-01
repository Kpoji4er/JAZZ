UndefineClass('P226')
DefineClass.P226 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 3-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 9,
	Reliability = 85,
	Icon = "Mod/e6L4ECj/WeaponIcons/P226.png",
	DisplayName = T(218461390224, --[[ModItemInventoryItemCompositeDef P226 DisplayName]] "P-226"),
	DisplayNamePlural = T(532649443806, --[[ModItemInventoryItemCompositeDef P226 DisplayNamePlural]] "P-226"),
	Description = T(337830409983, --[[ModItemInventoryItemCompositeDef P226 Description]] "Простой, точный и надежный, как швейцарские часы, парень очень хотел стать новым пистолетом для американской армии. Конкурс он проиграл, но не расстроился и занял оружейные почти всех остальных силовых структур Европы и США."),
	AdditionalHint = T(186387032377, --[[ModItemInventoryItemCompositeDef P226 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Куча обвесов"),
	UnitStat = "Marksmanship",
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 25,
	ObjDamageMod = 25,
	AimAccuracy = 10,
	CritChanceScaled = 25,
	MagazineSize = 15,
	WeaponRange = 21,
	OverwatchAngle = 5400,
	Entity = "P226ff",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagLarge_18_20",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_ImprovisedSuppressor",
				"JAZZ_PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"JAZZ_Freeswap",
			},
			'DefaultComponent', "JAZZ_Freeswap",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"JAZZ_BarrelShort_Pistol",
				"JAZZ_BarrelNormal",
			},
			'DefaultComponent', "JAZZ_BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handgrip",
			'AvailableComponents', {
				"JAZZ_Handgrip_Default",
				"JAZZ_Handgrip_Ergo",
			},
			'DefaultComponent', "JAZZ_Handgrip_Default",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_IronSight",
				"JAZZ_IronSight_AIM",
				"JAZZ_IronSight_FAST",
				"JAZZ_IronSight_NIGHT",
				"JAZZ_Reflex_Pistol",
			},
			'DefaultComponent', "JAZZ_IronSight",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_UVDot",
				"JAZZ_FlashlightDot",
			},
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
	ShootAP = 2000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 7,
	Grouping = 70,
	BaseJamChance = -100,
	WeaponResource = 3200,
	CanAppearUsed = false,
}

