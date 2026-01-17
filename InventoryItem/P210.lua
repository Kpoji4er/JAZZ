UndefineClass('P210')
DefineClass.P210 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 3,
	Reliability = 80,
	Icon = "Mod/e6L4ECj/WeaponIcons/P210.png",
	DisplayName = T(191783634543, --[[ModItemInventoryItemCompositeDef P210 DisplayName]] "P-210"),
	DisplayNamePlural = T(239088007136, --[[ModItemInventoryItemCompositeDef P210 DisplayNamePlural]] "P-210"),
	Description = T(931652226138, --[[ModItemInventoryItemCompositeDef P210 Description]] "Самый дорогой военный пистолет в мире, самый точный военный пистолет в мире, самый надежный военный пистолет в мире. Нельзя сказать, что самый редкий военный пистолет в мире, но стремится к этому."),
	AdditionalHint = T(310575798556, --[[ModItemInventoryItemCompositeDef P210 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пистолет швейцарской маминой подруги."),
	UnitStat = "Marksmanship",
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 22,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	CritChanceScaled = 40,
	MagazineSize = 8,
	WeaponRange = 18,
	OverwatchAngle = 5400,
	Noise = 22,
	Entity = "P210",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelLong",
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
			},
			'DefaultComponent', "Jazz_IronSight",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"FlashlightDot",
				"UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 22,
	BulletDropRange = 6,
	Grouping = 53,
	BaseJamChance = -50,
	WeaponResource = 1200,
}

