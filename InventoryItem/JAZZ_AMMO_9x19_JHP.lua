UndefineClass('JAZZ_AMMO_9x19_JHP')
DefineClass.JAZZ_AMMO_9x19_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919JHP.png",
	DisplayName = T(378106180006, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP DisplayName]] "9х19 мм, Luger JHP"),
	DisplayNamePlural = T(888021825675, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP DisplayNamePlural]] "9х19 мм, Luger JHP"),
	colorStyle = "AmmoHPColor",
	Description = T(442624820314, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_JHP Description]] "Гражданский патрон для стрельбы по тарелкам, бронебойности от него не дождешься, зато экспансивное действие хорошее, так что цельтесь в ноги, там много артерий!"),
	AdditionalHint = "",
	Cost = 360,
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
			mod_add = -2,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -6,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 60,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 25,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

