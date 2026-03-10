UndefineClass('M2Carbine')
DefineClass.M2Carbine = {
	__parents = { "Carbine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-1",
	object_class = "Carbine",
	ScrapParts = 8,
	RepairCost = 3,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/M2Carbine.png",
	DisplayName = T(142435704728, --[[ModItemInventoryItemCompositeDef M2Carbine DisplayName]] "Карбайн"),
	DisplayNamePlural = T(875798522299, --[[ModItemInventoryItemCompositeDef M2Carbine DisplayNamePlural]] "Карбайн"),
	Description = T(534013565696, --[[ModItemInventoryItemCompositeDef M2Carbine Description]] "Еще не настоящий промежуточный патрон, в том понимании, каким он был у СТГ-44 или Калашникова, но по концепции - очень даже настоящий промежуточный карабин. Меньше вес патрона - больше боекомплект. Больше боекомплект - выше плотность огня. Вот вам еще десантный вариант со складным прикладом, штурмовой с автоогнем, и специальный с ночным прицелом."),
	AdditionalHint = T(697050056619, --[[ModItemInventoryItemCompositeDef M2Carbine AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Может стрелять в движении \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Можно переделать в автомат \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 1750,
	CanAppearInShop = true,
	CategoryPair = "Rifles",
	Caliber = "JAZZ_Caliber_30CAL",
	Damage = 20,
	ObjDamageMod = 50,
	AimAccuracy = 9,
	MagazineSize = 30,
	WeaponRange = 36,
	OverwatchAngle = 1200,
	Noise = 30,
	HandSlot = "TwoHanded",
	Entity = "M2Carbine",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'AvailableComponents', {
				"StockLightFolded",
				"StockLightUnFolded",
				"StockNo",
				"StockNormal",
			},
			'DefaultComponent', "StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagSmall30_15",
			},
			'DefaultComponent', "MagSmall30_15",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"JAZZ_CombatScope_2x",
				"JAZZ_NightScope_M3",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Trigger",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Autofire",
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"FlashHider",
			},
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"SingleShot",
		"JAZZ_TargetSweep",
		"RunAndGun_Carbine",
	},
	ShootAP = 5000,
	ReloadAP = 6000,
	Recoil = 10,
	BurstShots = 2,
	AutoShots = 7,
	Handling = -10,
	BulletDropRange = 12,
	Grouping = 53,
	BaseJamChance = -100,
	WeaponResource = 3000,
}

