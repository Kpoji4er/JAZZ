UndefineClass('RPD')
DefineClass.RPD = {
	__parents = { "LightMachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "LightMachineGun",
	ScrapParts = 16,
	RepairCost = 8,
	Reliability = 70,
	Icon = "Mod/e6L4ECj/WeaponIcons/RPD.png",
	DisplayName = T(921726795014, --[[ModItemInventoryItemCompositeDef RPD DisplayName]] "РПД"),
	DisplayNamePlural = T(960477150592, --[[ModItemInventoryItemCompositeDef RPD DisplayNamePlural]] "РПД"),
	Description = T(214801991188, --[[ModItemInventoryItemCompositeDef RPD Description]] "Ручной пулемет Дегтярева (РПД) был разработан в 1944 году под новый на тот момент патрон 7.62х39 мм. Впоследствии был заменен на РПК, но успел широко распространиться по странам соцлагеря, так что до сих пор встречается на поле боя."),
	AdditionalHint = T(753688782220, --[[ModItemInventoryItemCompositeDef RPD AdditionalHint]] '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ручной пулемет под "семерку" \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В остальном средний'),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 9000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "MachineGuns",
	Caliber = "JAZZ_Caliber_762x39",
	Damage = 28,
	ObjDamageMod = 50,
	AimAccuracy = 10,
	MagazineSize = 100,
	WeaponRange = 40,
	OverwatchAngle = 600,
	Noise = 52,
	HandSlot = "TwoHanded",
	Entity = "RPD",
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
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_BarrelsDefs",
			},
			'DefaultComponent', "JAZZ_BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
			'DefaultComponent', "JAZZ_Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_IronSight",
			},
			'DefaultComponent', "JAZZ_IronSight",
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
	ShootAP = 9000,
	ReloadAP = 7000,
	WeaponMass = 80,
	CyclicRPM = 700,
	WeaponSizeClass = "Long",
	BurstLimiter = 0,
	Recoil = 18,
	BurstShots = 4,
	AutoShots = 7,

	CloseRange = 6,

	CloseRangeFactor = 85,
	BulletDropRange = 14,
	Grouping = 65,
	BaseJamChance = -10,
	WeaponResource = 9000,
}

