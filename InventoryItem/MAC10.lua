UndefineClass('MAC10')
DefineClass.MAC10 = {
	__parents = { "Autopistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "Autopistol",
	ScrapParts = 6,
	RepairCost = 4,
	Reliability = 70,
	Icon = "Mod/e6L4ECj/WeaponIcons/MAC10.png",
	DisplayName = T(612255777676, --[[ModItemInventoryItemCompositeDef MAC10 DisplayName]] "MAC-10"),
	DisplayNamePlural = T(799100522418, --[[ModItemInventoryItemCompositeDef MAC10 DisplayNamePlural]] "MAC-10"),
	Description = T(500943915358, --[[ModItemInventoryItemCompositeDef MAC10 Description]] "Компактный скорострельный американский автомат, сделанный под влиянием УЗИ. Его качества делают его максимально удобным для действий в замкнутых пространствах, заполненных людьми. Например, при захвате заложников в самолете. В смысле, освобождении захваченного самолета."),
	AdditionalHint = T(104635909892, --[[ModItemInventoryItemCompositeDef MAC10 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноручный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Складной приклад\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Скорострельный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Как УЗИшка, только не УЗИ"),
	UnitStat = "Marksmanship",
	Cost = 3000,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 150,
	CategoryPair = "SubmachineGuns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 27,
	ObjDamageMod = 25,
	AimAccuracy = 8,
	CritChanceScaled = 30,
	MagazineSize = 30,
	WeaponRange = 18,
	OverwatchAngle = 4680,
	Noise = 30,
	Entity = "MAC10",
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
				"JAZZ_PistolSuppressor",
				"JAZZ_Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"JAZZ_StockLightUnFolded",
				"JAZZ_StockLightFolded",
			},
			'DefaultComponent', "JAZZ_StockLightFolded",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"DualShot",
		"JAZZ_SmgStorm",
		"JAZZ_RunAndSMGStorm",
	},
	ShootAP = 4000,
	ReloadAP = 5000,
	MaxAimActions = 2,
	Recoil = 9,
	BurstShots = 5,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 6,
	Grouping = 72,
	BaseJamChance = -20,
	WeaponResource = 2700,
}

