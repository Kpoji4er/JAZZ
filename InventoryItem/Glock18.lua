UndefineClass('Glock18')
DefineClass.Glock18 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 70,
	Reliability = 60,
	Icon = "Mod/e6L4ECj/WeaponIcons/Glock18.png",
	DisplayName = T(876495756178, --[[ModItemInventoryItemCompositeDef Glock18 DisplayName]] "Glock 18"),
	DisplayNamePlural = T(478389428053, --[[ModItemInventoryItemCompositeDef Glock18 DisplayNamePlural]] "Glock 18"),
	Description = T(594387443300, --[[ModItemInventoryItemCompositeDef Glock18 Description]] "Glock 17 с переключателем в режим безудержного веселья и встроенным компенсатором. Автоматическая игрушка под патрон 9x19мм!"),
	AdditionalHint = T(358502954241, --[[ModItemInventoryItemCompositeDef Glock18 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бонус при стрельбе навскидку\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Особый режим стрельбы: короткая очередь\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность модификаций"),
	UnitStat = "Marksmanship",
	Cost = 15000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 40,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 18,
	ObjDamageMod = 15,
	AimAccuracy = 7,
	CritChance = 5,
	MagazineSize = 17,
	WeaponRange = 14,
	OverwatchAngle = 5400,
	Noise = 30,
	Entity = "G18",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ReflexSight",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
				"Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'Modifiable', false,
			'AvailableComponents', {
				"MuzzleBooster_Glock18",
			},
			'DefaultComponent', "MuzzleBooster_Glock18",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagLarge_17_33",
				"MagNormal",
				"MagNormalG18",
			},
			'DefaultComponent', "MagNormalG18",
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
		"BurstFire",
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 9,
	BurstShots = 4,
	AutoShots = 4,
	Handling = 100,
	BulletDropRange = 6,
	Grouping = 78,
	CanAppearUsed = false,
}

