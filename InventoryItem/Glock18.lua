UndefineClass('Glock18')
DefineClass.Glock18 = {
	__parents = { "Autopistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-5",
	object_class = "Autopistol",
	ScrapParts = 6,
	RepairCost = 15,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/Glock18.png",
	DisplayName = T(477797896110, --[[ModItemInventoryItemCompositeDef Glock18 DisplayName]] "Glock 18"),
	DisplayNamePlural = T(137749552678, --[[ModItemInventoryItemCompositeDef Glock18 DisplayNamePlural]] "Glock 18s"),
	Description = T(108518776488, --[[ModItemInventoryItemCompositeDef Glock18 Description]] "Glock 17 with a fun switch and built in compensator. 9x19mm spray in the palm of your hand. "),
	AdditionalHint = T(358502954241, --[[ModItemInventoryItemCompositeDef Glock18 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Быстрый  \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Компактный  \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Удобный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Прочный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Стреляет короткими очередями"),
	UnitStat = "Marksmanship",
	Cost = 15000,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 40,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 19,
	ObjDamageMod = 15,
	MagazineSize = 17,
	WeaponRange = 18,
	OverwatchAngle = 5400,
	Noise = 22,
	Entity = "G18",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ReflexSight",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"ImprovisedSuppressor",
				"PistolSuppressor",
				"Compensator",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'Modifiable', false,
			'AvailableComponents', {
				"MuzzleBooster_Glock18",
			},
			'DefaultComponent', "MuzzleBooster_Glock18",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagLarge_17_33",
				"MagNormal",
				"MagNormalG18",
			},
			'DefaultComponent', "MagNormalG18",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
				"FlashlightDot",
				"UVDot",
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
		"BurstFire",
		"SingleShot",
		"DualShot",
		"JAZZ_SmgStorm",
		"JAZZ_RunAndSMGStorm",
	},
	ShootAP = 2000,
	ReloadAP = 3000,
	MaxAimActions = 2,
	Recoil = 9,
	BurstShots = 4,
	AutoShots = 12,
	Handling = 22,
	BulletDropRange = 5,
	Grouping = 55,
	WeaponResource = 1500,
	CanAppearUsed = false,
}

