UndefineClass('JAZZ_AMMO_50BMG_HE')
DefineClass.JAZZ_AMMO_50BMG_HE = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_he",
	DisplayName = T(309974279653, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_HE DisplayName]] ".50, РАЗР"),
	DisplayNamePlural = T(322318596873, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_HE DisplayNamePlural]] ".50, РАЗР"),
	colorStyle = "AmmoHPColor",
	Description = T(642491927546, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_HE Description]] "Разрывной боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(549125160319, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_HE AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нулевая бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Высокий шанс критического попадания"),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_50BMG",
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
	ammo_type_icon = "UI/Icons/Items/ta_subsonic.png",
}

