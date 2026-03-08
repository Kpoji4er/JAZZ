UndefineClass('U100')
DefineClass.U100 = {
	__parents = { "LightMachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-1",
	object_class = "LightMachineGun",
	ScrapParts = 16,
	RepairCost = 8,
	Reliability = 65,
	Icon = "Mod/e6L4ECj/WeaponIcons/U100.png",
	DisplayName = T(266437267072, --[[ModItemInventoryItemCompositeDef U100 DisplayName]] "U100"),
	DisplayNamePlural = T(236944133476, --[[ModItemInventoryItemCompositeDef U100 DisplayNamePlural]] "U100"),
	Description = T(599878119827, --[[ModItemInventoryItemCompositeDef U100 Description]] 'Размышления на тему "если автомату дать длинный ствол и большой магазин, получится переавтомат или недопулемет?" из Сингапура. Вообще, за пулемет аргументов много - это и стрельба с заднего шептала, и сменный ствол. Питание из бубнов, конечно, но тут уж какие были ТЗ у заказчика.'),
	AdditionalHint = T(864604464205, --[[ModItemInventoryItemCompositeDef U100 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Легкий пулемет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Слабая отдача \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Большой магазин"),
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
	AimAccuracy = 10,
	MagazineSize = 30,
	WeaponRange = 48,
	OverwatchAngle = 840,
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
	AvailableAttacks = {
		"MGBurstFire",
		"BurstFire",
		"JAZZ_LargeAutoFire",
		"JAZZ_ControllableBurst",
		"JAZZ_TargetSweep",
	},
	ShootAP = 8000,
	ReloadAP = 6000,
	Recoil = 9,
	BurstShots = 4,
	AutoShots = 6,
	Handling = -20,
	BulletDropRange = 17,
	Grouping = 42,
	WeaponResource = 5500,
}

