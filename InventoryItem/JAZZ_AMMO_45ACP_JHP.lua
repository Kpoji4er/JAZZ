UndefineClass('JAZZ_AMMO_45ACP_JHP')
DefineClass.JAZZ_AMMO_45ACP_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPHP.png",
	DisplayName = T(587071959481, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP DisplayName]] ".45ACP, JHP"),
	DisplayNamePlural = T(993338998831, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP DisplayNamePlural]] ".45ACP, JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(582557259656, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP Description]] "Экспансивный патрон калибра .45ACP"),
	AdditionalHint = T(193100784452, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_JHP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 120,
	CanAppearInShop = true,
	MaxStock = 25,
	RestockWeight = 25,
	CategoryPair = "45ACP",
	ShopStackSize = 30,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

