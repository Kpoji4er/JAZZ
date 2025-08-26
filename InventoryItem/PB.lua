UndefineClass('PB')
DefineClass.PB = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-UNIQ",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 5,
	Reliability = 65,
	Icon = "Mod/e6L4ECj/WeaponIcons/PB.png",
	DisplayName = T(256183090542, --[[ModItemInventoryItemCompositeDef PB DisplayName]] "Пистолет ПБ"),
	DisplayNamePlural = T(809762590784, --[[ModItemInventoryItemCompositeDef PB DisplayNamePlural]] "Пистолеты ПБ"),
	Description = T(413605184956, --[[ModItemInventoryItemCompositeDef PB Description]] "Самый известный советский и российский пистолет. В современных реалиях его принято ругать, но чаще всего это делают те, кто стреляет разве что в монстров с экрана монитора."),
	AdditionalHint = T(181579765203, --[[ModItemInventoryItemCompositeDef PB AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшенные затраты ОД на выстрел\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный"),
	UnitStat = "Marksmanship",
	Cost = 450,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x18",
	Damage = 22,
	ObjDamageMod = 15,
	AimAccuracy = 10,
	CritChance = 5,
	CritChanceScaled = 35,
	MagazineSize = 8,
	WeaponRange = 16,
	OverwatchAngle = 5400,
	Noise = 2,
	Entity = "pb",
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
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 3000,
	ReloadAP = 4000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 80,
	BulletDropRange = 6,
	Grouping = 85,
	BaseJamChance = -100,
	WeaponResource = 3000,
}

