UndefineClass('JAZZ_AMMO_50BMG_SLAP')
DefineClass.JAZZ_AMMO_50BMG_SLAP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_slap",
	DisplayName = T(165082048360, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_SLAP DisplayName]] ".50, ПК"),
	DisplayNamePlural = T(987694579361, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_SLAP DisplayNamePlural]] ".50, ПК"),
	colorStyle = "AmmoAPColor",
	Description = T(280547274741, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_SLAP Description]] "Подкалиберный боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(442179722469, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_SLAP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Немного повышенный шанс критического попадания"),
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
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

