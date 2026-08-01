UndefineClass('Korth')
DefineClass.Korth = {
	__parents = { "Revolver" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 3-1",
	object_class = "Revolver",
	ScrapParts = 6,
	RepairCost = 25,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/Korth.png",
	DisplayName = T(890000000000523, --[[ModItemInventoryItemCompositeDef Korth DisplayName]] "Korth Revolver"),
	DisplayNamePlural = T(890000000000499, --[[ModItemInventoryItemCompositeDef Korth DisplayNamePlural]] "Korth Revolver"),
	Description = T(890000000001226, --[[ModItemInventoryItemCompositeDef Korth Description]] "Если вы закажете револьвер у компании Korth, то через 4-5 месяцев всего за 4000 долларов вы получите один из самых точных и надежных шестизарядников, которые только есть на планете Земля. Или можно за те же деньги купить десяток автоматов Калашникова, но это уж кто на что учился."),
	AdditionalHint = T(890000000000516, --[[ModItemInventoryItemCompositeDef Korth AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Револьвер\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Остальное не ваши проблемы"),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_357",
	Damage = 30,
	ObjDamageMod = 40,
	AimAccuracy = 19,
	CritChanceScaled = 30,
	MagazineSize = 6,
	WeaponRange = 24,
	OverwatchAngle = 5100,
	Noise = 32,
	Entity = "KorthRev",
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
				"JAZZ_BarrelLong",
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
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"JAZZ_Fanning",
		"JAZZ_Bullseye",
	},
	ShootAP = 3000,
	ReloadAP = 5000,
	MaxAimActions = 4,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 7,
	Grouping = 55,
	BaseJamChance = -100,
}

