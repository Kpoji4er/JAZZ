UndefineClass('APS')
DefineClass.APS = {
	__parents = { "Autopistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",

	comment = "Tier 2-4",
	object_class = "Autopistol",
	ScrapParts = 6,
	RepairCost = 10,
	Reliability = 55,
	Icon = "Mod/e6L4ECj/WeaponIcons/APS.png",
	DisplayName = T(762855095908, --[[ModItemInventoryItemCompositeDef APS DisplayName]] "Пистолет Стечкина"),
	DisplayNamePlural = T(791550858652, --[[ModItemInventoryItemCompositeDef APS DisplayNamePlural]] "Пистолеты Стечкина"),
	Description = T(803787536304, --[[ModItemInventoryItemCompositeDef APS Description]] "Маленькая ручная гаубица. Большой и серьезный советский пистолет, для офицеров, экипажей техники, артиллеристов и прочих, кому пистолета мало, а автомат не положен."),
	AdditionalHint = T(501438291047, --[[ModItemInventoryItemCompositeDef APS AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стреляет короткими очередями"),
	UnitStat = "Marksmanship",
	Cost = 6000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x18",
	Damage = 20,
	ObjDamageMod = 20,
	AimAccuracy = 12,
	MagazineSize = 18,
	WeaponRange = 17,
	OverwatchAngle = 5400,
	Noise = 19,
	Entity = "APS",
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
			'SlotType', "Barrel",
			'AvailableComponents', {
				"JAZZ_BarrelNormal_Sil",
				"JAZZ_BarrelNormal_noSil",
			},
			'DefaultComponent', "JAZZ_BarrelNormal_noSil",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"BurstFire",
		"SingleShot",
		"DualShot",
		"JAZZ_SmgStorm",
		"JAZZ_RunAndSMGStorm",
	},
	ShootAP = 3000,
	ReloadAP = 4000,
	WeaponMass = 30,
	CyclicRPM = 750,
	WeaponSizeClass = "Compact",
	BurstLimiter = 0,
	Recoil = 12,
	BurstShots = 4,
	AutoShots = 0,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 6,
	Grouping = 72,
	BaseJamChance = -20,
	WeaponResource = 2500,
}

