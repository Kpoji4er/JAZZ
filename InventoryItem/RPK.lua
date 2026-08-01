UndefineClass('RPK')
DefineClass.RPK = {
	__parents = { "LightMachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "LightMachineGun",
	ScrapParts = 16,
	RepairCost = 9,
	Reliability = 80,
	Icon = "Mod/e6L4ECj/WeaponIcons/RPK.png",
	DisplayName = T(940541298260, --[[ModItemInventoryItemCompositeDef RPK DisplayName]] "РПК"),
	DisplayNamePlural = T(300104203548, --[[ModItemInventoryItemCompositeDef RPK DisplayNamePlural]] "РПК"),
	Description = T(682256467954, --[[ModItemInventoryItemCompositeDef RPK Description]] "Ручной пулемет, созданный на платформе АК: конструкторы поставили ствол потолще и еще несколько модификаций, чтобы РПК мог вести непрерывный огонь. Этот пулемет должен был занять роль оружия поддержки на уровне взвода, учитывая простоту использования и совместимость магазинов с остальными «калашами»."),
	AdditionalHint = T(858142642339, --[[ModItemInventoryItemCompositeDef RPK AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Переавтомат-недопулемет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Недальнобойный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 10000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "MachineGuns",
	Caliber = "JAZZ_Caliber_762x39",
	Damage = 29,
	ObjDamageMod = 50,
	AimAccuracy = 10,
	MagazineSize = 30,
	WeaponRange = 42,
	OverwatchAngle = 840,
	Noise = 50,
	HandSlot = "TwoHanded",
	Entity = "Weapon_RPK74",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
			'DefaultComponent', "JAZZ_Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"JAZZ_BarrelNormal",
				"JAZZ_BarrelNormalImproved",
			},
			'DefaultComponent', "JAZZ_BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagLarge_30_40",
				"JAZZ_MagDrum_30-75",
			},
			'DefaultComponent', "JAZZ_MagLarge_30_40",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'AvailableComponents', {
				"JAZZ_RPK74_Hanguard_Basic",
				"JAZZ_RPK74_VerticalGrip",
			},
			'DefaultComponent', "JAZZ_RPK74_Hanguard_Basic",
		}),
				PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Compensator",
				"JAZZ_Suppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"MGBurstFire",
		"BurstFire",
		"JAZZ_ControllableBurst",
		"JAZZ_LargeAutoFire",
		"JAZZ_TargetSweep",
	},
	ShootAP = 8000,
	ReloadAP = 6000,
	Recoil = 10,
	BurstShots = 4,
	AutoShots = 7,

	CloseRange = 6,

	CloseRangeFactor = 85,
	BulletDropRange = 15,
	Grouping = 62,
	BaseJamChance = -30,
	WeaponResource = 12000,
}

