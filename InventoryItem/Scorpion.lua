UndefineClass('Scorpion')
DefineClass.Scorpion = {
	__parents = { "SubmachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "9x18 T1",
	object_class = "SubmachineGun",
	ScrapParts = 8,
	Icon = "Mod/e6L4ECj/WeaponIcons/Scorpion.png",
	DisplayName = T(389917013778, --[[ModItemInventoryItemCompositeDef Scorpion DisplayName]] "Scorpion"),
	DisplayNamePlural = T(505643276959, --[[ModItemInventoryItemCompositeDef Scorpion DisplayNamePlural]] "Scorpion"),
	Description = T(276327014875, --[[ModItemInventoryItemCompositeDef Scorpion Description]] "Маленький и удаленький чехословацкий автомат под советский пистолетный 9мм патрон. Оказался крайне удачным в использовании в контртеррористических операциях."),
	AdditionalHint = T(842942928399, --[[ModItemInventoryItemCompositeDef Scorpion AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноручное\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Складной приклад"),
	UnitStat = "Marksmanship",
	CanAppearInShop = true,
	RestockWeight = 50,
	CategoryPair = "SubmachineGuns",
	Caliber = "JAZZ_Caliber_9x18",
	Damage = 17,
	ObjDamageMod = 15,
	AimAccuracy = 7,
	CritChanceScaled = 5,
	MagazineSize = 20,
	WeaponRange = 15,
	OverwatchAngle = 4680,
	Entity = "Scorpion",
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
			'SlotType', "Stock",
			'AvailableComponents', {
				"StockLightFolded",
				"StockLightUnFolded",
			},
			'DefaultComponent', "StockLightFolded",
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
		"AutoFire",
		"SingleShot",
		"DualShot",
		"RunAndGun",
		"CancelShot",
	},
	ShootAP = 3000,
	ReloadAP = 4000,
	MaxAimActions = 2,
	Recoil = 4,
	BurstShots = 4,
	AutoShots = 8,
	Handling = 88,
	BulletDropRange = 6,
	Grouping = 70,
}

