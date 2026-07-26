UndefineClass('_50BMG_SLAP')
DefineClass._50BMG_SLAP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(328537436087, --[[ModItemInventoryItemCompositeDef _50BMG_SLAP DisplayName]] ".50 SLAP"),
	DisplayNamePlural = T(152196917983, --[[ModItemInventoryItemCompositeDef _50BMG_SLAP DisplayNamePlural]] ".50 SLAP"),
	colorStyle = "AmmoAPColor",
	Description = T(189786149121, --[[ModItemInventoryItemCompositeDef _50BMG_SLAP Description]] ".50 Ammo for Machine Guns, Snipers and Handguns."),
	AdditionalHint = T(181724059889, --[[ModItemInventoryItemCompositeDef _50BMG_SLAP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенная бронебойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Немного повышенный шанс критического попадания"),
	Cost = 500,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "50BMG",
	ShopStackSize = 10,
	MaxStacks = 5000,
	Caliber = "50BMG",
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

