UndefineClass('U100')
DefineClass.U100 = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "MachineGun",
	ScrapParts = 16,
	RepairCost = 8,
	Reliability = 60,
	Icon = "Mod/e6L4ECj/WeaponIcons/U100.png",
	DisplayName = T(266437267072, "U100"),
	DisplayNamePlural = T(236944133476, "U100"),
	Description = T(599878119827, 'Размышления на тему "если автомату дать длинный ствол и большой магазин, получится переавтомат или недопулемет?" из Сингапура. Вообще, за пулемет аргументов много - это и стрельба с заднего шептала, и сменный ствол. Питание из бубнов, конечно, но тут уж какие были ТЗ у заказчика.'),
	AdditionalHint = T(864604464205, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Легкий"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 12000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "MachineGuns",
	Caliber = "JAZZ_Caliber_556",
	Damage = 21,
	ObjDamageMod = 50,
	AimAccuracy = 20,
	CritChance = 5,
	MagazineSize = 100,
	WeaponRange = 48,
	Noise = 48,
	HandSlot = "TwoHanded",
	Entity = "U100",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'AvailableComponents', {
				"FoldBipod",
				"UnfoldBipod",
			},
			'DefaultComponent', "FoldBipod",
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
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagDrum_30-100",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Mountfront",
			'Modifiable', false,
			'AvailableComponents', {
				"U100Handle",
			},
			'DefaultComponent', "U100Handle",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'AvailableComponents', {
				"DefMuzzle",
			},
			'DefaultComponent', "DefMuzzle",
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
	ShootAP = 7000,
	ReloadAP = 6000,
	Recoil = 7,
	BurstShots = 6,
	AutoShots = 6,
	Handling = 50,
	BulletDropRange = 17,
	Grouping = 272,
	WeaponResource = 5500,
}

