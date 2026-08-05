UndefineClass('MAC2429')
DefineClass.MAC2429 = {
	__parents = { "LightMachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-1",
	object_class = "LightMachineGun",
	ScrapParts = 12,
	RepairCost = 1,
	Icon = "Mod/e6L4ECj/WeaponIcons/2429.png",
	DisplayName = T(354142133889, --[[ModItemInventoryItemCompositeDef MAC2429 DisplayName]] "Mac 2429"),
	DisplayNamePlural = T(582831103058, --[[ModItemInventoryItemCompositeDef MAC2429 DisplayNamePlural]] "Mac 2429"),
	Description = T(476500872548, --[[ModItemInventoryItemCompositeDef MAC2429 Description]] "Французский ручной пулемет, использовавшийся французской армией во второй мировой войне. Такой небольшой опыт эксплуатации не позволил составить какое-то единое мнение о качествах оружия."),
	AdditionalHint = T(777023896289, --[[ModItemInventoryItemCompositeDef MAC2429 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Легкий пулемет \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сильная отдача \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ненадежный \n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Убойный"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Cost = 3000,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 40,
	CategoryPair = "MachineGuns",
	CanAppearStandard = false,
	Caliber = "JAZZ_Caliber_75French",
	Damage = 33,
	ObjDamageMod = 80,
	AimAccuracy = 7,
	MagazineSize = 25,
	WeaponRange = 56,
	OverwatchAngle = 840,
	Noise = 68,
	HandSlot = "TwoHanded",
	Entity = "MAC2429",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'AvailableComponents', {
				"JAZZ_Bipod",
			},
			'DefaultComponent', "JAZZ_Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_BarrelsDefs",
			},
			'DefaultComponent', "JAZZ_BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_StockNormal",
			},
			'DefaultComponent', "JAZZ_StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"JAZZ_MagNormal",
			},
			'DefaultComponent', "JAZZ_MagNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"MGBurstFire",
		"BurstFire",
		"JAZZ_ControllableBurst",
		"JAZZ_LargeAutoFire",
		"JAZZ_TargetSweep",
	},
	ShootAP = 8000,
	ReloadAP = 7000,
	WeaponMass = 80,
	CyclicRPM = 700,
	WeaponSizeClass = "Long",
	BurstLimiter = 0,
	Recoil = 18,
	BurstShots = 4,
	AutoShots = 7,

	CloseRange = 8,

	CloseRangeFactor = 85,
	BulletDropRange = 14,
	Grouping = 32,
	WeaponResource = 2400,
}

