UndefineClass('JAZZ_AMMO_40mmFlashbangGrenade')
DefineClass.JAZZ_AMMO_40mmFlashbangGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_flashbang_grenade",
	DisplayName = T(921485234830, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFlashbangGrenade DisplayName]] "40-мм с/ш граната"),
	DisplayNamePlural = T(179422312087, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFlashbangGrenade DisplayNamePlural]] "40-мм с/ш гранаты"),
	Description = T(585104380446, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFlashbangGrenade Description]] "Светошумовой боеприпас для гранатометов калибра 40 мм."),
	AdditionalHint = T(308173152169, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFlashbangGrenade AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В эпицентре взрыва снижает уровень энергии целей (один раз за бой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> <color EmStyle>Подавляет</color> цели\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Издает меньше шума"),
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 30,
	CategoryPair = "Ordnance",
	MaxStacks = 6,
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
	Caliber = "JAZZ_Caliber_40mmGrenade",
	BaseDamage = 5,
	Noise = 5,
	Entity = "Weapon_MilkorMGL_Shell",
}

