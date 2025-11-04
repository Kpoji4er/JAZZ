UndefineClass('Auto5_quest')
DefineClass.Auto5_quest = {
	__parents = { "Shotgun" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Shotgun",
	ScrapParts = 10,
	RepairCost = 50,
	Reliability = 20,
	Icon = "UI/Icons/Weapons/Auto5Quest",
	ItemType = "Shotgun",
	DisplayName = T(649146508338, "«Усмиритель» Мамаши"),
	DisplayNamePlural = T(432332068612, "«Усмирители» Мамаши"),
	Description = T(580584506617, "Легендарная владелица бара в Порт-Какао, Мамаша Бакстер, использовала этот кастомный дробовик Auto-5, чтобы заканчивать кабацкие драки максимально эффективным и ультимативным способом."),
	AdditionalHint = T(269691251565, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Быстрое усмирение"),
	LargeItem = 1,
	Valuable = 1,
	Cost = 1200,
	RestockWeight = 0,
	Caliber = "12gauge",
	Damage = 4,
	ObjDamageMod = 150,
	AimAccuracy = 4,
	MagazineSize = 9,
	WeaponRange = 8,
	PointBlankBonus = 1,
	OverwatchAngle = 1200,
	BuckshotConeAngle = 1200,
	BuckshotFalloffDamage = 100,
	HandSlot = "TwoHanded",
	Entity = "Weapon_Auto5",
	ComponentSlots = {
		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Barrel",
			'AvailableComponents', {
				"Auto5_Basic_LMag",
			},
			'DefaultComponent', "Auto5_Basic_LMag",
		}),
	},
	HolsterSlot = "Shoulder",
	AvailableAttacks = {
		"Buckshot",
	},
	ShootAP = 4000,
	ReloadAP = 3000,
	BurstShots = 1,
	AutoShots = 1,
}

