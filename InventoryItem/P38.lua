UndefineClass('P38')
DefineClass.P38 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 3,
	Icon = "Mod/e6L4ECj/WeaponIcons/P38.png",
	DisplayName = T(848119151903, --[[ModItemInventoryItemCompositeDef P38 DisplayName]] "P38"),
	DisplayNamePlural = T(927743133237, --[[ModItemInventoryItemCompositeDef P38 DisplayNamePlural]] "P38"),
	Description = T(107106412369, --[[ModItemInventoryItemCompositeDef P38 Description]] 'Спортивный, боевой, полицейский, гражданский пистолет из Чехии. Практически, победитель оружейного "Евровидения", но первое место принадлежит тому, кого нельзя называть. Иначе придется его купить.'),
	AdditionalHint = T(491343014488, --[[ModItemInventoryItemCompositeDef P38 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая точность"),
	UnitStat = "Marksmanship",
	Cost = 1250,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 20,
	ObjDamageMod = 20,
	AimAccuracy = 10,
	CritChance = 5,
	CritChanceScaled = 35,
	MagazineSize = 8,
	WeaponRange = 18,
	OverwatchAngle = 5400,
	Noise = 18,
	Entity = "P38",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"MagNormal",
				"MagLarge",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelNormal",
				"BarrelShort_Pistol",
			},
			'DefaultComponent', "BarrelNormal",
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
	BulletDropRange = 6,
	Grouping = 94,
	BaseJamChance = -20,
}

