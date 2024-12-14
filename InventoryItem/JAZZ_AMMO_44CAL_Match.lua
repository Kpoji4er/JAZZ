UndefineClass('JAZZ_AMMO_44CAL_Match')
DefineClass.JAZZ_AMMO_44CAL_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/44MATCH.png",
	DisplayName = T(189935598461, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match DisplayName]] ".44, Match"),
	DisplayNamePlural = T(807918005698, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match DisplayNamePlural]] ".44, Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(821434202204, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match Description]] "Матчевый патрон для револьверов и винтовок калибра .44."),
	AdditionalHint = T(283032175872, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_44CAL_Match AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность стрельбы без штрафов"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 25,
	RestockWeight = 25,
	CategoryPair = "44CAL",
	ShopStackSize = 12,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_44CAL",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Grouping",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

