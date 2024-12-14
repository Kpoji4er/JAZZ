UndefineClass('_40mmFlashbangGrenade')
DefineClass._40mmFlashbangGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_flashbang_grenade",
	DisplayName = T(725404168171, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade DisplayName]] "40-мм с/ш граната"),
	DisplayNamePlural = T(197284197871, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade DisplayNamePlural]] "40-мм с/ш гранаты"),
	Description = T(288672948029, --[[ModItemInventoryItemCompositeDef _40mmFlashbangGrenade Description]] "Светошумовой боеприпас для гранатометов калибра 40 мм."),
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
		"IncreaseTiredness",
		"Suppressed",
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

