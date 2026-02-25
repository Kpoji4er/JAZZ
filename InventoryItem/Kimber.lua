UndefineClass('Kimber')
DefineClass.Kimber = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 6,
	Reliability = 65,
	Icon = "Mod/e6L4ECj/WeaponIcons/Kimber.png",
	DisplayName = T(646219544697, --[[ModItemInventoryItemCompositeDef Kimber DisplayName]] "Kimber"),
	DisplayNamePlural = T(539052887945, --[[ModItemInventoryItemCompositeDef Kimber DisplayNamePlural]] "Kimber"),
	Description = T(239186058142, --[[ModItemInventoryItemCompositeDef Kimber Description]] "Очередной 1911 современного исполнения, отлично подходящий и для охоты и для спортивной стрельбы. Для снижения мощной отдачи патрона применяется компенсатор оригинальной конструкции. Используется с коллиматорным прицелом."),
	AdditionalHint = T(123923849772, --[[ModItemInventoryItemCompositeDef Kimber AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> С коллиматором\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Понтовый"),
	UnitStat = "Marksmanship",
	Cost = 600,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 29,
	ObjDamageMod = 25,
	AimAccuracy = 7,
	CritChanceScaled = 30,
	MagazineSize = 7,
	WeaponRange = 15,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "Kimber",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
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
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_7_10",
			},
			'DefaultComponent', "MagNormal",
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
			'SlotType', "Scope",
			'AvailableComponents', {
				"Jazz_IronSight",
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
			},
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
		"PistolPerk_Mozambique",
		"PistolPerk_TrickShotRun",
	},
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 18,
	BulletDropRange = 5,
	Grouping = 59,
	BaseJamChance = -10,
	WeaponResource = 1400,
}

