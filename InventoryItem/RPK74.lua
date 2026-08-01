UndefineClass('RPK74')
DefineClass.RPK74 = {
	__parents = { "LightMachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-4",
	object_class = "LightMachineGun",
	ScrapParts = 16,
	RepairCost = 12,
	Reliability = 85,
	Icon = "Mod/e6L4ECj/WeaponIcons/RPK74.png",
	DisplayName = T(679005533471, --[[ModItemInventoryItemCompositeDef RPK74 DisplayName]] "РПК-74"),
	DisplayNamePlural = T(500616509541, --[[ModItemInventoryItemCompositeDef RPK74 DisplayNamePlural]] "РПК-74"),
	Description = T(897065949753, --[[ModItemInventoryItemCompositeDef RPK74 Description]] "РПК-74 - это разработанный в пару автомату АК-74 ручной пулемет под новый тогда малоимпульсный патрон 5.45х39. Как и РПК, от базового автомата отличается усиленной ствольной коробкой и тяжелым стволом, что расширяет дальность огневого поражения отделения до 600 метров."),
	AdditionalHint = T(317702044957, --[[ModItemInventoryItemCompositeDef RPK74 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Переавтомат-недопулемет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Слабая отдача"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 75000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 2,
	RestockWeight = 30,
	CategoryPair = "MachineGuns",
	Caliber = "JAZZ_Caliber_545",
	Damage = 26,
	ObjDamageMod = 50,
	AimAccuracy = 12,
	MagazineSize = 30,
	WeaponRange = 50,
	PointBlankBonus = 1,
	OverwatchAngle = 840,
	Noise = 48,
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
				"JAZZ_MagLarge_30_45",
			},
			'DefaultComponent', "JAZZ_MagLarge_30_45",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'Modifiable', false,
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
			},
			'DefaultComponent', "JAZZ_Compensator",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_StockNormal",
				"JAZZ_StockLight",
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
	Recoil = 8,
	BurstShots = 4,
	AutoShots = 7,

	CloseRange = 6,

	CloseRangeFactor = 85,
	BulletDropRange = 18,
	Grouping = 56,
	BaseJamChance = -30,
	WeaponResource = 11500,
}

