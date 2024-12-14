UndefineClass('P210')
DefineClass.P210 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1 9mm",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 70,
	Icon = "Mod/e6L4ECj/WeaponIcons/P210.png",
	DisplayName = T(191783634543, --[[ModItemInventoryItemCompositeDef P210 DisplayName]] "P-210"),
	DisplayNamePlural = T(239088007136, --[[ModItemInventoryItemCompositeDef P210 DisplayNamePlural]] "P-210"),
	Description = T(931652226138, --[[ModItemInventoryItemCompositeDef P210 Description]] "Самый дорогой военный пистолет в мире, самый точный военный пистолет в мире, самый надежный военный пистолет в мире. Нельзя сказать, что самый редкий военный пистолет в мире, но стремится к этому."),
	AdditionalHint = T(310575798556, --[[ModItemInventoryItemCompositeDef P210 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая точность"),
	UnitStat = "Marksmanship",
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 21,
	ObjDamageMod = 20,
	AimAccuracy = 9,
	CritChance = 5,
	CritChanceScaled = 40,
	MagazineSize = 8,
	WeaponRange = 14,
	OverwatchAngle = 5400,
	Noise = 30,
	Entity = "p210",
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
	Handling = 98,
	BulletDropRange = 6,
	Grouping = 95,
	BaseJamChance = -50,
}

