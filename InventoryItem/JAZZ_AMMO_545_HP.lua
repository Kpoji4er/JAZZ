UndefineClass('JAZZ_AMMO_545_HP')
DefineClass.JAZZ_AMMO_545_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "HP - Гражданские. Дамажат, но не пробивают",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545HP.png",
	DisplayName = T(402352878282, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_HP DisplayName]] "5,45 мм, HP"),
	DisplayNamePlural = T(875634951024, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_HP DisplayNamePlural]] "5,45 мм, HP"),
	colorStyle = "AmmoHPColor",
	Description = T(979485744753, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_HP Description]] "Гражданский спортивно-охотничий патрон калибра 5.45x39мм."),
	AdditionalHint = T(692375443733, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Уменьшенное пробитие"),
	Cost = 90,
	CanAppearInShop = true,
	CategoryPair = "545",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "CritChance",
		}),
	},
}

