UndefineClass('JAZZ_AMMO_9x19_Match')
DefineClass.JAZZ_AMMO_9x19_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919McH.png",
	DisplayName = T(109553390621, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match DisplayName]] "9х19 мм, Match 124gr OTM"),
	DisplayNamePlural = T(108637483108, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match DisplayNamePlural]] "9х19 мм, Match 124gr OTM"),
	colorStyle = "AmmoMatchColor",
	Description = T(644299617955, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_Match Description]] "Вы когда-нибудь пробовали снайпинг из беретты или глока? Обязательно попробуйте, данный боеприпас позволит вам стрелять кучнее и дальше, чем прочие гражданские или самодельные. Бронебойность отсутствует как и у большинства пистолетных патронов, чуда не ждите."),
	AdditionalHint = "",
	Cost = 900,
	CanAppearInShop = true,
	MaxStock = 15,
	RestockWeight = 10,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1180,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

