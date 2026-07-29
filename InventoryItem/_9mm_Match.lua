UndefineClass('_9mm_Match')
DefineClass._9mm_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(557669429065, --[[ModItemInventoryItemCompositeDef _9mm_Match DisplayName]] "9х19 мм, Match"),
	DisplayNamePlural = T(909118059097, --[[ModItemInventoryItemCompositeDef _9mm_Match DisplayNamePlural]] "9х19 мм, Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(203032964857, --[[ModItemInventoryItemCompositeDef _9mm_Match Description]] "Матчевый патрон калибра 9х19мм"),
	AdditionalHint = T(169382118769, --[[ModItemInventoryItemCompositeDef _9mm_Match AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность стрельбы без штрафов"),
	Cost = 350,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 120,
	Caliber = "9mm",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

