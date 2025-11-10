UndefineClass('P226')
DefineClass.P226 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 3-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 9,
	Reliability = 30,
	Icon = "Mod/e6L4ECj/WeaponIcons/P226.png",
	DisplayName = T(218461390224, --[[ModItemInventoryItemCompositeDef P226 DisplayName]] "P-226"),
	DisplayNamePlural = T(532649443806, --[[ModItemInventoryItemCompositeDef P226 DisplayNamePlural]] "P-226"),
	Description = T(337830409983, --[[ModItemInventoryItemCompositeDef P226 Description]] "Простой, точный и надежный, как швейцарские часы, парень очень хотел стать новым пистолетом для американской армии. Конкурс он проиграл, но не расстроился и занял оружейные почти всех остальных силовых структур Европы и США."),
	AdditionalHint = T(186387032377, --[[ModItemInventoryItemCompositeDef P226 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая точность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность модификаций"),
	UnitStat = "Marksmanship",
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 21,
	ObjDamageMod = 25,
	AimAccuracy = 10,
	CritChanceScaled = 25,
	MagazineSize = 15,
	WeaponRange = 19,
	OverwatchAngle = 5400,
	Entity = "P226ff",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_18_20",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelShort_Pistol",
				"BarrelNormal",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handgrip",
			'AvailableComponents', {
				"Handgrip_Default",
				"Handgrip_Ergo",
			},
			'DefaultComponent', "Handgrip_Default",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"Jazz_IronSight",
				"Jazz_IronSight_AIM",
				"Jazz_IronSight_FAST",
				"Jazz_IronSight_NIGHT",
				"JAZZ_Reflex_Pistol",
			},
			'DefaultComponent', "Jazz_IronSight",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"UVDot",
				"FlashlightDot",
			},
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 2000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 96,
	BulletDropRange = 6,
	Grouping = 88,
	BaseJamChance = -100,
	WeaponResource = 3200,
	CanAppearUsed = false,
}

