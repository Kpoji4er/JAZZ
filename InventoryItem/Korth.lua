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
	DisplayName = T(436628869426, "Korth Revolver"),
	DisplayNamePlural = T(427566606201, "Korth Revolver"),
	Description = T(878461703337, "Если вы закажете револьвер у компании Korth, то через 4-5 месяцев всего за 4000 долларов вы получите один из самых точных и надежных шестизарядников, которые только есть на планете Земля. Или можно за те же деньги купить десяток автоматов Калашникова, но это уж кто на что учился."),
	AdditionalHint = T(434107786112, "Баюн не сделал описание этому предмету :("),
	UnitStat = "Marksmanship",
	Cost = 500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_357",
	Damage = 30,
	ObjDamageMod = 40,
	AimAccuracy = 20,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 6,
	OverwatchAngle = 5100,
	Noise = 32,
	Entity = "KorthRev",
	ComponentSlots = {
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
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 3000,
	ReloadAP = 5000,
	Recoil = 1,
	AutoShots = 3,
	Handling = 88,
	BulletDropRange = 7,
	Grouping = 92,
	BaseJamChance = -100,
}

