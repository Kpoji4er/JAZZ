UndefineClass('SWModel29')
DefineClass.SWModel29 = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 4,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/SWModel29.png",
	DisplayName = T(890000000000525, --[[ModItemInventoryItemCompositeDef SWModel29 DisplayName]] "SWModel29"),
	DisplayNamePlural = T(890000000000502, --[[ModItemInventoryItemCompositeDef SWModel29 DisplayNamePlural]] "SWModel29"),
	Description = T(890000000001227, --[[ModItemInventoryItemCompositeDef SWModel29 Description]] "Мощный револьвер Смита и Вессона под патрон .44 Magnum. Как и другие подобные револьверы повышенной мощности прежде всего применяется для охоты или спортивной стрельбы, но... как же приятно засадить Легу в жбан из сорок четвертого."),
	AdditionalHint = T(890000000000518, --[[ModItemInventoryItemCompositeDef SWModel29 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Револьвер \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сорок четвертый \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_44CAL",
	Damage = 42,
	ObjDamageMod = 40,
	AimAccuracy = 10,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 19,
	OverwatchAngle = 5100,
	Noise = 32,
	Entity = "SWModel29",
	ComponentSlots = {
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
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
			},
		}),
	},
	Color = "Black",
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"JAZZ_Fanning",
		"JAZZ_Bullseye",
	},
	ShootAP = 4000,
	ReloadAP = 5000,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 7,
	Grouping = 68,
	BaseJamChance = -100,
}

