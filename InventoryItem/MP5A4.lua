UndefineClass('MP5A4')
DefineClass.MP5A4 = {
	__parents = { "SubmachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-5",
	object_class = "SubmachineGun",
	ScrapParts = 8,
	RepairCost = 12,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/MP5A4.png",
	DisplayName = T(123316525310, --[[ModItemInventoryItemCompositeDef MP5A4 DisplayName]] "MP5A4"),
	DisplayNamePlural = T(897337319220, --[[ModItemInventoryItemCompositeDef MP5A4 DisplayNamePlural]] "MP5A4"),
	Description = T(903859276526, --[[ModItemInventoryItemCompositeDef MP5A4 Description]] "Современный вариант автомата MP5, допускающий стрельбу как с отсечкой по три выстрела, так и полностью автоматический огонь. Все остальное осталось практически без изменений, автомат сразу хорошим получился."),
	AdditionalHint = T(545249677427, --[[ModItemInventoryItemCompositeDef MP5A4 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Теперь с фонариком"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 7000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 60,
	CategoryPair = "SubmachineGuns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 23,
	ObjDamageMod = 20,
	AimAccuracy = 13,
	MagazineSize = 30,
	WeaponRange = 30,
	OverwatchAngle = 4320,
	Noise = 28,
	HandSlot = "TwoHanded",
	Entity = "MP5A4",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagSmall30_15",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Reflex_Aimpoint5000",
				"JAZZ_Reflex_Closed",
				"JAZZ_Reflex_Open",
				"JAZZ_Reflex_M68",
				"JAZZ_Reflex_Eotech",
				"JAZZ_CombatScope_2x",
				"JAZZ_CombatScope_FeroZ24",
				"JAZZ_Scope_DA15_6x",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"JAZZ_StockLightFolded",
				"JAZZ_StockLightUnFolded",
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
			},
			'DefaultComponent', "JAZZ_Flashlight",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"RunAndGun",
		"JAZZ_Zipper",
	},
	ShootAP = 4000,
	ReloadAP = 4000,
	Recoil = 3,
	AutoShots = 8,
	BulletDropRange = 10,

	CloseRange = 2,

	CloseRangeFactor = 95,
	Grouping = 72,
	BaseJamChance = -30,
	WeaponResource = 5500,
	CanAppearUsed = false,
}

