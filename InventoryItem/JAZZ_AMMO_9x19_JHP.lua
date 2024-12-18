UndefineClass('JAZZ_AMMO_9x19_JHP')
DefineClass.JAZZ_AMMO_9x19_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919JHP.png",
	DisplayName = T(378106180006, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP DisplayName]] "9х19 мм, JHP"),
	DisplayNamePlural = T(888021825675, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP DisplayNamePlural]] "9х19 мм, JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(442624820314, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP Description]] "Экспансивный патрон калибра 9х19мм"),
	AdditionalHint = T(932865416694, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>"),
	Cost = 120,
	CanAppearInShop = true,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
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

