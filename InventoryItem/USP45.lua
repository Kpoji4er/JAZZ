UndefineClass('USP45')
DefineClass.USP45 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T3 45acp",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 4,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/USP45.png",
	DisplayName = T(280616524895, --[[ModItemInventoryItemCompositeDef USP45 DisplayName]] "USP45 Tactical"),
	DisplayNamePlural = T(840364522187, --[[ModItemInventoryItemCompositeDef USP45 DisplayNamePlural]] "USP45 Tactical"),
	Description = T(875880547954, --[[ModItemInventoryItemCompositeDef USP45 Description]] "Пистолет с грубыми формами, но с тонкой душевной организацией. Одних только вариантов УСМ, в зависимости от места службы, может быть более дюжины. Прочен, как будто сделан из адамантия."),
	AdditionalHint = T(846027870607, --[[ModItemInventoryItemCompositeDef USP45 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий урон и шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Бонус при стрельбе навскидку\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность модификаций"),
	UnitStat = "Marksmanship",
	Cost = 2500,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 26,
	ObjDamageMod = 25,
	AimAccuracy = 10,
	CritChance = 10,
	CritChanceScaled = 45,
	MagazineSize = 12,
	WeaponRange = 16,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "USP45",
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
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'AvailableComponents', {
				"JAZZ_Reflex_Pistol",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"UVDot",
				"FlashlightDot",
			},
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
	Handling = 96,
	BulletDropRange = 6,
	Grouping = 95,
	BaseJamChance = -20,
	WeaponResource = 2000,
	CanAppearUsed = false,
}

