UndefineClass('Bereta92')
DefineClass.Bereta92 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T2",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 70,
	Reliability = 20,
	Icon = "Mod/e6L4ECj/WeaponIcons/Beretta92.png",
	DisplayName = T(589617789927, --[[ModItemInventoryItemCompositeDef Bereta92 DisplayName]] "Beretta 92F"),
	DisplayNamePlural = T(237291598806, --[[ModItemInventoryItemCompositeDef Bereta92 DisplayNamePlural]] "Beretta 92F"),
	Description = T(424449219883, --[[ModItemInventoryItemCompositeDef Bereta92 Description]] "Беретта - пистолет с ярко выраженным запахом нуара. Плохие полицейские, хорошие полицейские, которые тоже плохие, дорогие женщины, опасные женщины, мертвые женщины. Они все мертвы. Последний выстрел поставил жирную точку в этой истории..."),
	AdditionalHint = T(759493287779, --[[ModItemInventoryItemCompositeDef Bereta92 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность модификаций"),
	UnitStat = "Marksmanship",
	Cost = 1500,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_9x19",
	Damage = 20,
	ObjDamageMod = 20,
	AimAccuracy = 8,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 17,
	WeaponRange = 14,
	OverwatchAngle = 5400,
	Entity = "Weapon_Beretta92F",
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
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagLarge",
				"MagNormal",
			},
			'DefaultComponent', "MagNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"BarrelLong",
				"BarrelNormal",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Flashlight",
				"LaserDot",
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
	Handling = 99,
	BulletDropRange = 7,
	Grouping = 89,
	BaseJamChance = -10,
}

