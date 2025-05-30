UndefineClass('MP446VIKING')
DefineClass.MP446VIKING = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T2",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 70,
	Reliability = 30,
	Icon = "Mod/e6L4ECj/WeaponIcons/Viking.png",
	DisplayName = T(310685586669, --[[ModItemInventoryItemCompositeDef MP446VIKING DisplayName]] 'MP-446 "Викинг"'),
	DisplayNamePlural = T(202717539367, --[[ModItemInventoryItemCompositeDef MP446VIKING DisplayNamePlural]] 'MP-446 "Викинг"'),
	Description = T(963661589708, --[[ModItemInventoryItemCompositeDef MP446VIKING Description]] 'Гражданская и спортивная версия российского армейского пистолета Ярыгина. Само по себе словосочетание "гражданский пистолет в России" выглядит насмешкой над предполагаемыми пользователями оружия, но на экспорт-то продавать его никто не запрещает.'),
	AdditionalHint = T(974784958890, --[[ModItemInventoryItemCompositeDef MP446VIKING AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бонус при стрельбе навскидку"),
	UnitStat = "Marksmanship",
	Cost = 1600,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 22,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 17,
	WeaponRange = 14,
	OverwatchAngle = 5400,
	Entity = "Viking",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"BarrelsDefs",
			},
			'DefaultComponent', "BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'AvailableComponents', {
				"LaserDot",
				"Flashlight",
				"FlashlightDot",
				"UVDot",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
		}),
	},
	HolsterSlot = "Leg",
	AvailableAttacks = {
		"SingleShot",
		"DualShot",
		"CancelShot",
		"MobileShot",
	},
	ShootAP = 3000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,
	Handling = 95,
	BulletDropRange = 6,
	Grouping = 88,
	BaseJamChance = -20,
}

