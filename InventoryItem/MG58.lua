UndefineClass('MG58')
DefineClass.MG58 = {
	__parents = { "MachineGun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Tier 1-UNIQ",
	object_class = "MachineGun",
	ScrapParts = 12,
	RepairCost = 5,
	Reliability = 60,
	Icon = "UI/Icons/Weapons/MG58.png",
	DisplayName = T(915870069225, "MG58"),
	DisplayNamePlural = T(728744819234, "MG58"),
	Description = T(207644767915, "Модифицированный MG42 со стволом из композитума-58, улучшенным прицелом и рядом доработок механизма. Встречайте: MG58. "),
	AdditionalHint = T(714045001218, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тяжелый"),
	LargeItem = 1,
	Cumbersome = 1,
	UnitStat = "Marksmanship",
	Valuable = 1,
	Cost = 5000,
	Caliber = "JAZZ_Caliber_792",
	Damage = 38,
	ObjDamageMod = 80,
	AimAccuracy = 22,
	MagazineSize = 50,
	WeaponRange = 56,
	OverwatchAngle = 1800,
	Noise = 75,
	HandSlot = "TwoHanded",
	Entity = "Weapon_MG42",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Bipod",
			'Modifiable', false,
			'AvailableComponents', {
				"Bipod_MG42",
			},
			'DefaultComponent', "Bipod_MG42",
		}),
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Scope",
			'Modifiable', false,
			'AvailableComponents', {
				"ImprovedIronsight",
			},
			'DefaultComponent', "ImprovedIronsight",
		}),
	},
	HolsterSlot = "Shoulder",
	PreparedAttackType = "Machine Gun",
	AvailableAttacks = {
		"MGBurstFire",
	},
	ShootAP = 8000,
	ReloadAP = 8000,
	Handling = 35,
	BulletDropRange = 26,
	Grouping = 292,
	WeaponResource = 8000,
}

