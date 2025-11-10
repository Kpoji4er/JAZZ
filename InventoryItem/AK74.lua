UndefineClass('AK74')
DefineClass.AK74 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "AssaultRifle",
	ScrapParts = 10,
	RepairCost = 10,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/AK74.png",
	DisplayName = T(489350715496, --[[ModItemInventoryItemCompositeDef AK74 DisplayName]] "АК74"),
	DisplayNamePlural = T(261108237192, --[[ModItemInventoryItemCompositeDef AK74 DisplayNamePlural]] "АК74"),
	Description = T(903430945152, --[[ModItemInventoryItemCompositeDef AK74 Description]] "В районе 1974 года советские конструкторы обновили классический дизайн «калаша» - так и появился на свет этот красавец. В него внесли много изменений, но сердце механизма - газовый поршень длинного хода - осталось в оригинальном виде."),
	AdditionalHint = T(216627067101, --[[ModItemInventoryItemCompositeDef AK74 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая эффективность при стрельбе очередями\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая надежность"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 60000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 40,
	CategoryPair = "AssaultRifles",
	Caliber = "JAZZ_Caliber_545",
	Damage = 25,
	ObjDamageMod = 45,
	AimAccuracy = 24,
	CritChanceScaled = 20,
	MagazineSize = 30,
	WeaponRange = 48,
	OverwatchAngle = 1320,
	Noise = 49,
	HandSlot = "TwoHanded",
	Entity = "AK74",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"StockNormal",
				"StockLightFolded",
				"StockLightUnFolded",
			},
			'DefaultComponent', "StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'Modifiable', false,
			'AvailableComponents', {
				"Handguard",
			},
			'DefaultComponent', "Handguard",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_30_45",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Under",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"GP25",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'AvailableComponents', {
				"Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Bipod",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Scope_PSO",
				"JAZZ_Reflex_Cobra",
				"JAZZ_Reflex_PKAS",
				"JAZZ_CombatScope_1P29",
				"JAZZ_NightScope_NSPU",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"CancelShot",
	},
	ShootAP = 5000,
	ReloadAP = 6000,
	Recoil = 7,
	AutoShots = 6,
	Handling = 66,
	BulletDropRange = 18,
	Grouping = 270,
	BaseJamChance = -50,
	WeaponResource = 9800,
}

