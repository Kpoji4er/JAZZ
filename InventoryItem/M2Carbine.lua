UndefineClass('M2Carbine')
DefineClass.M2Carbine = {
	__parents = { "Carbine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-1",
	object_class = "Carbine",
	ScrapParts = 8,
	RepairCost = 3,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/M2Carbine.png",
	DisplayName = T(142435704728, --[[ModItemInventoryItemCompositeDef M2Carbine DisplayName]] "Карбайн"),
	DisplayNamePlural = T(875798522299, --[[ModItemInventoryItemCompositeDef M2Carbine DisplayNamePlural]] "Карбайн"),
	Description = T(890000000000671, --[[ModItemInventoryItemCompositeDef M2Carbine Description]] "Еще не настоящий промежуточный патрон, в том понимании, каким он был у СТГ-44 или Калашникова, но по концепции - очень даже настоящий промежуточный карабин. Меньше вес патрона - больше боекомплект. Больше боекомплект - выше плотность огня. Вот вам еще десантный вариант со складным прикладом, штурмовой с автоогнем, и специальный с ночным прицелом."),
	AdditionalHint = T(890000000000915, --[[ModItemInventoryItemCompositeDef M2Carbine AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Может стрелять в движении \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно переделать в автомат \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 2400,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 100,
	CategoryPair = "Rifles",
	Caliber = "JAZZ_Caliber_30CAL",
	Damage = 23,
	ObjDamageMod = 50,
	AimAccuracy = 9,
	MagazineSize = 30,
	WeaponRange = 36,
	OverwatchAngle = 1200,
	Noise = 30,
	HandSlot = "TwoHanded",
	Entity = "M2Carbine",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"JAZZ_StockLightFolded",
				"JAZZ_StockLightUnFolded",
				"JAZZ_StockNo",
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagSmall30_15_M2CARBINE",
			},
			'DefaultComponent', "JAZZ_MagSmall30_15_M2CARBINE",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_CombatScope_2x",
				"JAZZ_NightScope_M3",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Trigger",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Autofire",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_FlashHider",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_TargetSweep",
		"RunAndGun_Carbine",
	},
	ShootAP = 5000,
	ReloadAP = 6000,
	WeaponMass = 28,
	CyclicRPM = 750,
	WeaponSizeClass = "Carbine",
	BurstLimiter = 0,
	Recoil = 19,
	BurstShots = 4,
	AutoShots = 8,

	CloseRange = 5,

	CloseRangeFactor = 90,
	BulletDropRange = 12,
	Grouping = 53,
	BaseJamChance = -100,
	WeaponResource = 3000,
}

