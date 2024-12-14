UndefineClass('RPK')
DefineClass.RPK = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1+",
	object_class = "MachineGun",
	ScrapParts = 16,
	Reliability = 95,
	Icon = "Mod/e6L4ECj/WeaponIcons/RPK.png",
	DisplayName = T(940541298260, --[[ModItemInventoryItemCompositeDef RPK DisplayName]] "РПК"),
	DisplayNamePlural = T(300104203548, --[[ModItemInventoryItemCompositeDef RPK DisplayNamePlural]] "РПК"),
	Description = T(682256467954, --[[ModItemInventoryItemCompositeDef RPK Description]] "Ручной пулемет, созданный на платформе АК: конструкторы поставили ствол потолще и еще несколько модификаций, чтобы РПК мог вести непрерывный огонь. Этот пулемет должен был занять роль оружия поддержки на уровне взвода, учитывая простоту использования и совместимость магазинов с остальными «калашами»."),
	AdditionalHint = T(858142642339, --[[ModItemInventoryItemCompositeDef RPK AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Легкий (без бубна)"),
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
	AimAccuracy = 19,
	MagazineSize = 30,
	WeaponRange = 42,
	Noise = 55,
	HandSlot = "TwoHanded",
	Entity = "Weapon_RPK74",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Bipod",
			},
			'DefaultComponent', "Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"BarrelNormal",
				"BarrelNormalImproved",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_30_40",
				"MagDrum_30-75",
			},
			'DefaultComponent', "MagLarge_30_40",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'AvailableComponents', {
				"RPK74_Hanguard_Basic",
				"RPK74_VerticalGrip",
			},
			'DefaultComponent', "RPK74_Hanguard_Basic",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"LROptics",
				"ReflexSight",
				"ScopeCOG",
				"ThermalScope",
				"LROpticsAdvanced",
				"ScopeCOGQuick",
				"ReflexSightAdvanced",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Compensator",
				"Suppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"StockNormal",
			},
			'DefaultComponent', "StockNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	PreparedAttackType = "Machine Gun",
	AvailableAttacks = {
		"MGBurstFire",
	},
	ShootAP = 5000,
	ReloadAP = 5000,
	Recoil = 8,
	BurstShots = 4,
	AutoShots = 4,
	Handling = 70,
	BulletDropRange = 15,
	Grouping = 270,
	BaseJamChance = -30,
}

