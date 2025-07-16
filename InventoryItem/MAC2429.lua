UndefineClass('MAC2429')
DefineClass.MAC2429 = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1-",
	object_class = "MachineGun",
	ScrapParts = 12,
	RepairCost = 1,
	Reliability = 15,
	Icon = "Mod/e6L4ECj/WeaponIcons/2429.png",
	DisplayName = T(354142133889, --[[ModItemInventoryItemCompositeDef MAC2429 DisplayName]] "Mac 2429"),
	DisplayNamePlural = T(582831103058, --[[ModItemInventoryItemCompositeDef MAC2429 DisplayNamePlural]] "Mac 2429"),
	Description = T(476500872548, --[[ModItemInventoryItemCompositeDef MAC2429 Description]] "Французский ручной пулемет, использовавшийся французской армией во второй мировой войне. Такой небольшой опыт эксплуатации не позволил составить какое-то единое мнение о качествах оружия."),
	AdditionalHint = T(777023896289, --[[ModItemInventoryItemCompositeDef MAC2429 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Легкий\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Ржавый"),
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
	AimAccuracy = 16,
	MagazineSize = 25,
	WeaponRange = 56,
	Noise = 68,
	HandSlot = "TwoHanded",
	Entity = "MAC2429",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'Modifiable', false,
			'AvailableComponents', {
				"Bipod",
			},
			'DefaultComponent', "Bipod",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"BarrelsDefs",
			},
			'DefaultComponent', "BarrelsDefs",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"StockNormal",
			},
			'DefaultComponent', "StockNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'Modifiable', false,
			'AvailableComponents', {
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
	},
	HolsterSlot = "Shoulder",
	PreparedAttackType = "Machine Gun",
	AvailableAttacks = {
		"MGBurstFire",
	},
	ShootAP = 5000,
	ReloadAP = 5000,
	Recoil = 32,
	BurstShots = 4,
	AutoShots = 4,
	Handling = 24,
	BulletDropRange = 19,
	Grouping = 260,
	WeaponResource = 2400,
}

