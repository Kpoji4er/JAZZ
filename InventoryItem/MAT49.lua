UndefineClass('MAT49')
DefineClass.MAT49 = {
	__parents = { "SubmachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-1",
	object_class = "SubmachineGun",
	ScrapParts = 6,
	RepairCost = 1,
	Reliability = 45,
	Icon = "Mod/e6L4ECj/WeaponIcons/MAT49.png",
	DisplayName = T(892229243751, --[[ModItemInventoryItemCompositeDef MAT49 DisplayName]] "MAT-49"),
	DisplayNamePlural = T(714310548316, --[[ModItemInventoryItemCompositeDef MAT49 DisplayNamePlural]] "MAT-49"),
	Description = T(303318756297, --[[ModItemInventoryItemCompositeDef MAT49 Description]] "Небольшой послевоенный французский автомат, широко распространенный в бывших французких колониях. Ничем особо примечательным не выделяется, нареканий особых тоже не имеет. Стреляет, и ладно."),
	AdditionalHint = T(561861858971, --[[ModItemInventoryItemCompositeDef MAT49 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неудобный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Неточный\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Старый\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Складной приклад\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>  Что досталось в оружейке"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 500,
	CategoryPair = "SubmachineGuns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 16,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	MagazineSize = 32,
	WeaponRange = 24,
	OverwatchAngle = 3960,
	Noise = 32,
	HandSlot = "TwoHanded",
	Entity = "MAT49",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_StockLightFolded",
				"JAZZ_StockLightUnFolded",
			},
			'DefaultComponent', "JAZZ_StockLightUnFolded",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"RunAndGun",
		"JAZZ_Zipper",
	},
	ShootAP = 5000,
	ReloadAP = 5000,
	MaxAimActions = 2,
	Recoil = 5,
	AutoShots = 6,

	CloseRange = 2,

	CloseRangeFactor = 95,
	BulletDropRange = 8,
	Grouping = 28,
	BaseJamChance = 50,
	WeaponResource = 1200,
}

