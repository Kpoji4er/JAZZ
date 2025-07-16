UndefineClass('Colt1911')
DefineClass.Colt1911 = {
	__parents = { "Pistol" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "T1 45acp",
	object_class = "Pistol",
	ScrapParts = 6,
	RepairCost = 6,
	Reliability = 50,
	Icon = "Mod/e6L4ECj/WeaponIcons/1911.png",
	DisplayName = T(646219544697, --[[ModItemInventoryItemCompositeDef Colt1911 DisplayName]] "Colt M1911"),
	DisplayNamePlural = T(539052887945, --[[ModItemInventoryItemCompositeDef Colt1911 DisplayNamePlural]] "Colt M1911"),
	Description = T(239186058142, --[[ModItemInventoryItemCompositeDef Colt1911 Description]] 'Дедушка недавно отметил 100-летний юбилей, но уходить куда-то вовсе не собирается, пока, дословно "не изобретут эти ваши лазеры-шмазеры и световые мечи".'),
	AdditionalHint = T(123923849772, --[[ModItemInventoryItemCompositeDef Colt1911 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий урон"),
	UnitStat = "Marksmanship",
	Cost = 600,
	CanAppearInShop = true,
	CategoryPair = "Handguns",
	Caliber = "JAZZ_Caliber_45ACP",
	Damage = 25,
	ObjDamageMod = 25,
	AimAccuracy = 7,
	CritChance = 5,
	CritChanceScaled = 30,
	MagazineSize = 7,
	WeaponRange = 15,
	OverwatchAngle = 5400,
	Noise = 28,
	Entity = "Colt1911",
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
			},
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Freeswap",
			'AvailableComponents', {
				"Freeswap",
			},
			'DefaultComponent', "Freeswap",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Side",
			'AvailableComponents', {
				"Flashlight",
			},
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
	Handling = 92,
	BulletDropRange = 5,
	Grouping = 92,
	BaseJamChance = -10,
	WeaponResource = 1400,
}

