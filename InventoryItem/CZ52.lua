UndefineClass('CZ52')
DefineClass.CZ52 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-2",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 1,
	Reliability = 45,
	Icon = "Mod/e6L4ECj/WeaponIcons/CZ52.png",
	DisplayName = T(890000000001148, --[[ModItemInventoryItemCompositeDef CZ52 DisplayName]] "CZ Vz. 52"),
	DisplayNamePlural = T(890000000001288, --[[ModItemInventoryItemCompositeDef CZ52 DisplayNamePlural]] "CZ Vz. 52"),
	Description = T(890000000000009, --[[ModItemInventoryItemCompositeDef CZ52 Description]] "Не особо популярный чехословацкий пистолет. На стандартных патронах 7.62х25мм, рассчитанных на повышенное давление в стволе, происходил чрезвычайно быстрый износ, что могло приводить к самопроизвольным выстрелам."),
	AdditionalHint = T(890000000000609, --[[ModItemInventoryItemCompositeDef CZ52 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ненадежный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Малый магазин\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дальнобойный"),
	UnitStat = "Marksmanship",
	Cost = 1250,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_762x25",
	Damage = 20,
	ObjDamageMod = 20,
	AimAccuracy = 6,
	CritChanceScaled = 35,
	MagazineSize = 8,
	WeaponRange = 21,
	OverwatchAngle = 5400,
	Noise = 22,
	Entity = "CZ52",
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
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_LaserDot",
				"JAZZ_FlashlightDot",
				"JAZZ_UVDot",
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
	MaxAimActions = 2,
	Recoil = 1,
	AutoShots = 3,

	CloseRange = 0,

	CloseRangeFactor = 100,
	BulletDropRange = 8,
	Grouping = 56,
	BaseJamChance = -20,
	WeaponResource = 650,
}

