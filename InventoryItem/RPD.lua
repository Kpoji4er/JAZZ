UndefineClass('RPD')
DefineClass.RPD = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T2-",
	object_class = "MachineGun",
	ScrapParts = 16,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/RPD.png",
	DisplayName = T(921726795014, --[[ModItemInventoryItemCompositeDef RPD DisplayName]] "РПД"),
	DisplayNamePlural = T(960477150592, --[[ModItemInventoryItemCompositeDef RPD DisplayNamePlural]] "РПД"),
	Description = T(214801991188, --[[ModItemInventoryItemCompositeDef RPD Description]] "Ручной пулемет Дегтярева (РПД) был разработан в 1944 году под новый на тот момент патрон 7.62х39 мм. Впоследствии был заменен на РПК, но успел широко распространиться по странам соцлагеря, так что до сих пор встречается на поле боя."),
	AdditionalHint = T(753688782220, --[[ModItemInventoryItemCompositeDef RPD AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тяжелый"),
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
	AimAccuracy = 20,
	MagazineSize = 100,
	WeaponRange = 40,
	OverwatchAngle = 1800,
	Noise = 52,
	HandSlot = "TwoHanded",
	Entity = "RPD",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"BarrelsDefs",
			},
			'DefaultComponent', "BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"StockNormal",
			},
			'DefaultComponent', "StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'AvailableComponents', {
				"FoldBipod",
				"UnfoldBipod",
			},
			'DefaultComponent', "UnfoldBipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"Jazz_IronSight",
			},
			'DefaultComponent', "Jazz_IronSight",
		}),
	},
	HolsterSlot = "Shoulder",
	PreparedAttackType = "Machine Gun",
	AvailableAttacks = {
		"MGBurstFire",
	},
	ShootAP = 6000,
	ReloadAP = 5000,
	Recoil = 10,
	BurstShots = 6,
	AutoShots = 6,
	Handling = 40,
	BulletDropRange = 14,
	Grouping = 250,
	BaseJamChance = -10,
	WeaponResource = 9000,
}

