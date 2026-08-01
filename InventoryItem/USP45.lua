UndefineClass('USP45')
DefineClass.USP45 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 4,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/USP45.png",
	DisplayName = T(280616524895, --[[ModItemInventoryItemCompositeDef USP45 DisplayName]] "USP45 Tactical"),
	DisplayNamePlural = T(840364522187, --[[ModItemInventoryItemCompositeDef USP45 DisplayNamePlural]] "USP45 Tactical"),
	Description = T(875880547954, --[[ModItemInventoryItemCompositeDef USP45 Description]] "Пистолет с грубыми формами, но с тонкой душевной организацией. Одних только вариантов УСМ, в зависимости от места службы, может быть более дюжины. Прочен, как будто сделан из адамантия."),
	AdditionalHint = T(846027870607, --[[ModItemInventoryItemCompositeDef USP45 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Долговечный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ультранадежный"),
	UnitStat = "Marksmanship",
	Cost = 2500,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 29,
	ObjDamageMod = 25,
	AimAccuracy = 11,
	CritChanceScaled = 45,
	MagazineSize = 12,
	WeaponRange = 18,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "USP45",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
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
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_Reflex_Pistol",
			},
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
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 8,
	Grouping = 88,
	BaseJamChance = -20,
	WeaponResource = 2000,
	CanAppearUsed = false,
}

