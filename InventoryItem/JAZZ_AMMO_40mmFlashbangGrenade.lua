UndefineClass('JAZZ_AMMO_40mmFlashbangGrenade')
DefineClass.JAZZ_AMMO_40mmFlashbangGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_flashbang_grenade",
	DisplayName = T(921485234830, "40-мм с/ш граната"),
	DisplayNamePlural = T(179422312087, "40-мм с/ш гранаты"),
	Description = T(585104380446, "Светошумовой боеприпас для гранатометов калибра 40 мм."),
	AdditionalHint = T(308173152169, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В эпицентре взрыва снижает уровень энергии целей (один раз за бой)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> <color EmStyle>Подавляет</color> цели\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Издает меньше шума"),
	Cost = 800,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "Ordnance",
	MaxStacks = 6,
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
	Caliber = "JAZZ_Caliber_40mmGrenade",
	BaseDamage = 5,
	Noise = 5,
	Entity = "Weapon_MilkorMGL_Shell",
}

