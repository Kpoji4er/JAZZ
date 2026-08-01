UndefineClass('M24Sniper')
DefineClass.M24Sniper = {
	__parents = { "SniperRifle" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 2-5",
	object_class = "SniperRifle",
	ScrapParts = 14,
	RepairCost = 7,
	Reliability = 90,
	Icon = "Mod/e6L4ECj/WeaponIcons/M24.png",
	DisplayName = T(672666400702, --[[ModItemInventoryItemCompositeDef M24Sniper DisplayName]] "M24"),
	DisplayNamePlural = T(703533260621, --[[ModItemInventoryItemCompositeDef M24Sniper DisplayNamePlural]] "M24s"),
	Description = T(767131106202, --[[ModItemInventoryItemCompositeDef M24Sniper Description]] "US Army sniper weapon system that replaced the M21 (based on the M14). Apparently semi-auto was still not up to par with what snipers needed in terms of reliability and accuracy that bolt action can provide. "),
	AdditionalHint = T(268336330579, --[[ModItemInventoryItemCompositeDef M24Sniper AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Винтовка с ручным перезаряжанием \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Медленно стреляет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Надежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Точный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 35000,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Rifles",
	Caliber = "JAZZ_Caliber_762x51",
	Damage = 37,
	ObjDamageMod = 80,
	AimAccuracy = 17,
	CritChanceScaled = 50,
	MagazineSize = 5,
	WeaponRange = 85,
	OverwatchAngle = 420,
	Noise = 46,
	HandSlot = "TwoHanded",
	Entity = "Weapon_M24",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"JAZZ_StockHeavy",
				"JAZZ_StockLight",
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"JAZZ_MagNormal",
				"JAZZ_MagLarge_5_10",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_CombatScope_2x",
				"JAZZ_CombatScope_ACOG",
				"JAZZ_NightScope",
				"JAZZ_Scope_6x",
				"JAZZ_Scope_12x",
				"JAZZ_Scope_Scout",
			},
			'DefaultComponent', "JAZZ_Scope_6x",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Suppressor",
				"JAZZ_SuppressorImproved",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_Flashlight",
				"JAZZ_FlashlightDot",
				"JAZZ_LaserDot",
				"JAZZ_UVDot",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_JokerShot",
		"JAZZ_Bullseye",
	},
	ShootAP = 8000,
	ReloadAP = 7000,
	BurstShots = 1,
	AutoShots = 1,

	CloseRange = 12,

	CloseRangeFactor = 70,
	BulletDropRange = 21,
	Grouping = 46,
	BaseJamChance = -20,
	WeaponResource = 5500,
}

