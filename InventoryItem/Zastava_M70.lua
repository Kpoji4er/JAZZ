UndefineClass('Zastava_M70')
DefineClass.Zastava_M70 = {
	__parents = { "AssaultRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "AssaultRifle",
	ScrapParts = 10,
	RepairCost = 20,
	Reliability = 65,
	Icon = "Mod/e6L4ECj/WeaponIcons/ZastavaM70.png",
	DisplayName = T(781657382465, --[[ModItemInventoryItemCompositeDef Zastava_M70 DisplayName]] "Zastava M70"),
	DisplayNamePlural = T(288131795255, --[[ModItemInventoryItemCompositeDef Zastava_M70 DisplayNamePlural]] "Zastava M70"),
	Description = T(387786738837, --[[ModItemInventoryItemCompositeDef Zastava_M70 Description]] "Югославская лицензионная копия советского автомата АКМ. Братушки не стали изобретать велосипед, и в итоге их автоматы почти такие же классные, как и советские. Из заметных отличий разве что устройство для стрельбы винтовочными гранатами, остальной обвес полностью взаимозаменяем."),
	AdditionalHint = T(272774945644, --[[ModItemInventoryItemCompositeDef Zastava_M70 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая эффективность автоматической стрельбы"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 5200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 150,
	CategoryPair = "AssaultRifles",
	Caliber = "JAZZ_Caliber_762x39",
	Damage = 28,
	ObjDamageMod = 50,
	AimAccuracy = 19,
	CritChance = 5,
	MagazineSize = 30,
	WeaponRange = 38,
	OverwatchAngle = 1800,
	Noise = 44,
	HandSlot = "TwoHanded",
	Entity = "Zastava_M70",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"StockLightFolded",
				"StockLightUnFolded",
			},
			'DefaultComponent', "StockLightUnFolded",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "General",
			'Modifiable', false,
			'AvailableComponents', {
				"M70_Unfld_GL",
				"M70_Fld_GL",
			},
			'DefaultComponent', "M70_Fld_GL",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge_30_40",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Bipod",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'CanBeEmpty', true,
			'AvailableComponents', {
				"M70_Grenade",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
	},
	ShootAP = 5000,
	ReloadAP = 5000,
	Recoil = 15,
	AutoShots = 6,
	Handling = 70,
	BulletDropRange = 14,
	Grouping = 238,
	BaseJamChance = -20,
	WeaponResource = 8600,
}

