UndefineClass('JAZZ_AMMO_9x19_Match')
DefineClass.JAZZ_AMMO_9x19_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919McH.png",
	DisplayName = T(109553390621, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match DisplayName]] "9х19 мм, Match"),
	DisplayNamePlural = T(108637483108, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match DisplayNamePlural]] "9х19 мм, Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(644299617955, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match Description]] "Матчевый патрон калибра 9х19мм"),
	AdditionalHint = T(212673832639, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная дальность стрельбы без штрафов"),
	Cost = 350,
	CanAppearInShop = true,
	MaxStock = 15,
	RestockWeight = 25,
	CategoryPair = "9mm",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

