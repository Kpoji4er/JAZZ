UndefineClass('Kimber')
DefineClass.Kimber = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 6,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/1911.png",
	DisplayName = T(646219544697, --[[ModItemInventoryItemCompositeDef Kimber DisplayName]] "Kimber DEV"),
	DisplayNamePlural = T(539052887945, --[[ModItemInventoryItemCompositeDef Kimber DisplayNamePlural]] "Kimber DEV"),
	Description = T(239186058142, --[[ModItemInventoryItemCompositeDef Kimber Description]] "Очередной 1911 современного исполнения, отлично подходящий и для охоты и для спортивной стрельбы. Для снижения мощной отдачи патрона применяется компенсатор оригинальной конструкции. Используется с коллиматорным прицелом."),
	AdditionalHint = T(123923849772, --[[ModItemInventoryItemCompositeDef Kimber AdditionalHint]] "Баюн не сделал описание этому предмету :("),
	UnitStat = "Marksmanship",
	Cost = 600,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 29,
	ObjDamageMod = 25,
	AimAccuracy = 10,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 7,
	WeaponRange = 15,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "Colt1911",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
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
			'SlotType', "Side",
			'AvailableComponents', {
				"Flashlight",
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
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 88,
	BulletDropRange = 5,
	Grouping = 92,
	BaseJamChance = -10,
	WeaponResource = 1400,
}

