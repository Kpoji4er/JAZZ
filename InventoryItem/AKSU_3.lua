UndefineClass('AKSU_3')
DefineClass.AKSU_3 = {
	__parents = { "SubmachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T2+",
	object_class = "SubmachineGun",
	ScrapParts = 10,
	RepairCost = 50,
	Reliability = 80,
	Icon = "Mod/e6L4ECj/\\WeaponIcons/aksu_4.png",
	DisplayName = T(247679453964, "АКС-74У 2"),
	DisplayNamePlural = T(674950846950, "АКС-74У"),
	Description = T(789741936265, "Укороченная версия AK-74, предназначенная для бойцов спецназа и экипажей техники. Для нее пришлось разработать новый газовый двигатель и дульное устройство-дожигатель. Американцы называют эту модель «Krinkov», но у русских в ходу более звучные названия - «Ксюха», а иногда и «Сучка». И да, для АКСУ существует набедренная кобура."),
	AdditionalHint = T(942349814086, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Возможность вести маневренный бой\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокая точность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс крита"),
	LargeItem = 1,
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 7500,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 40,
	CategoryPair = "SubmachineGuns",
	Caliber = "545",
	Damage = 24,
	AimAccuracy = 5,
	CritChance = 10,
	CritChanceScaled = 20,
	MagazineSize = 30,
	WeaponRange = 34,
	PointBlankBonus = 1,
	OverwatchAngle = 1448,
	Noise = 55,
	HandSlot = "TwoHanded",
	Entity = "Weapon_AKS74U",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'Modifiable', false,
			'AvailableComponents', {
				"BarrelNormal",
			},
			'DefaultComponent', "BarrelNormal",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'AvailableComponents', {
				"AKSU_Hanguard_Basic",
				"AKSU_VerticalGrip",
			},
			'DefaultComponent', "AKSU_Hanguard_Basic",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Magazine",
			'AvailableComponents', {
				"MagNormal",
				"MagLarge",
			},
			'DefaultComponent', "MagNormal",
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
			'SlotType', "Muzzle",
			'CanBeEmpty', true,
			'AvailableComponents', {
				"Compensator",
				"ImprovisedSuppressor",
			},
			'DefaultComponent', "Compensator",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Stock",
			'Modifiable', false,
			'AvailableComponents', {
				"StockLight",
			},
			'DefaultComponent', "StockLight",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"BurstFire",
		"AutoFire",
		"SingleShot",
		"RunAndGun",
		"CancelShot",
	},
	ShootAP = 4000,
	ReloadAP = 5000,
	Recoil = 12,
	AutoShots = 6,
	EffectiveRange = 5,
}

