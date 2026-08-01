UndefineClass('CZ75')
DefineClass.CZ75 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-3",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 7,
	Reliability = 75,
	Icon = "Mod/e6L4ECj/WeaponIcons/CZ75.png",
	DisplayName = T(890000000001147, --[[ModItemInventoryItemCompositeDef CZ75 DisplayName]] "CZ75"),
	DisplayNamePlural = T(890000000001287, --[[ModItemInventoryItemCompositeDef CZ75 DisplayNamePlural]] "CZ75"),
	Description = T(890000000000011, --[[ModItemInventoryItemCompositeDef CZ75 Description]] 'Спортивный, боевой, полицейский, гражданский пистолет из Чехии. Практически, победитель оружейного "Евровидения", но первое место принадлежит тому, кого нельзя называть. Иначе придется его купить.'),
	AdditionalHint = T(890000000000610, --[[ModItemInventoryItemCompositeDef CZ75 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Безопасный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Чемпионский"),
	UnitStat = "Marksmanship",
	Cost = 1250,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 24,
	ObjDamageMod = 20,
	AimAccuracy = 12,
	CritChanceScaled = 35,
	MagazineSize = 16,
	OverwatchAngle = 5400,
	Noise = 24,
	Entity = "CZ75",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagLarge",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'Modifiable', false,
			'CanBeEmpty', true,
			'AvailableComponents', {
								"JAZZ_ImprovisedSuppressor",
								"JAZZ_Suppressor",
							},
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
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 7,
	Grouping = 72,
	BaseJamChance = -20,
	WeaponResource = 1500,
}

