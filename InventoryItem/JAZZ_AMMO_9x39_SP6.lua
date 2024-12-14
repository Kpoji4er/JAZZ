UndefineClass('JAZZ_AMMO_9x39_SP6')
DefineClass.JAZZ_AMMO_9x39_SP6 = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СП6",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/939SP6.png",
	DisplayName = T(508580108192, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP6 DisplayName]] "9x39 мм, бронебойные"),
	DisplayNamePlural = T(724138101974, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP6 DisplayNamePlural]] "9x39 мм, бронебойные"),
	colorStyle = "AmmoAPColor",
	Description = T(343666682437, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP6 Description]] "Советский специальный бронебойный боеприпас СП6 калибра 9х39мм"),
	AdditionalHint = T(483938895844, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x39_SP6 AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 4-м классом брони"),
	Cost = 900,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 10,
	RestockWeight = 10,
	CategoryPair = "556",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_9x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "PenetrationClass",
		}),
	},
}

