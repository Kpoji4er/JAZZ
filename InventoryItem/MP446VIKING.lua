UndefineClass('MP446VIKING')
DefineClass.MP446VIKING = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 5,
	Reliability = 60,
	Icon = "Mod/e6L4ECj/WeaponIcons/Viking.png",
	DisplayName = T(310685586669, --[[ModItemInventoryItemCompositeDef MP446VIKING DisplayName]] 'MP-446 "Викинг"'),
	DisplayNamePlural = T(202717539367, --[[ModItemInventoryItemCompositeDef MP446VIKING DisplayNamePlural]] 'MP-446 "Викинг"'),
	Description = T(963661589708, --[[ModItemInventoryItemCompositeDef MP446VIKING Description]] 'Гражданская и спортивная версия российского армейского пистолета Ярыгина. Само по себе словосочетание "гражданский пистолет в России" выглядит насмешкой над предполагаемыми пользователями оружия, но на экспорт-то продавать его никто не запрещает.'),
	AdditionalHint = T(974784958890, --[[ModItemInventoryItemCompositeDef MP446VIKING AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Спортивный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тонированный "),
	UnitStat = "Marksmanship",
	Cost = 1600,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 25,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	CritChanceScaled = 30,
	MagazineSize = 17,
	WeaponRange = 19,
	OverwatchAngle = 5400,
	Noise = 24,
	Entity = "Viking",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_BarrelsDefs",
			},
			'DefaultComponent', "JAZZ_BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'AvailableComponents', {
				"JAZZ_ImprovisedSuppressor",
				"JAZZ_PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'AvailableComponents', {
				"JAZZ_LaserDot",
				"JAZZ_Flashlight",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"JAZZ_Freeswap",
			},
			'DefaultComponent', "JAZZ_Freeswap",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"MobileShot",
		"JAZZ_Mozambique",
		"JAZZ_DoubleTap",
	},
	ShootAP = 3000,
	ReloadAP = 4000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 7,
	Grouping = 68,
	BaseJamChance = -20,
	WeaponResource = 1800,
}

