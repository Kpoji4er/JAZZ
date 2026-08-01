UndefineClass('_40mmFlashbangGrenade')
DefineClass._40mmFlashbangGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(805412560134, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade DisplayName]] "40 mm Flashbang"),
	DisplayNamePlural = T(753721174279, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade DisplayNamePlural]] "40 mm Flashbangs"),
	Description = T(637064167762, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade Description]] "40 mm ordnance ammo for Grenade Launchers."),
	AdditionalHint = T(523265065541, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В эпицентре взрыва снижает уровень энергии целей (один раз за бой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> <color EmStyle>Подавляет</color> цели\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Издает меньше шума"),
	Cost = 800,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	CenterUnitDamageMod = 130,
	CenterObjDamageMod = 10,
	CenterAppliedEffects = {
		"IncreaseTirednessSuppressed",
	},
	AreaObjDamageMod = 10,
	AreaAppliedEffects = {
		"Suppressed",
	},
	PenetrationClass = 1,
	BurnGround = false,
	Caliber = "40mmGrenade",
	BaseDamage = 5,
	Noise = 5,
	Entity = "Weapon_MilkorMGL_Shell",
}

