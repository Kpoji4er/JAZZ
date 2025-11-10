UndefineClass('JAZZ_AMMO_9x18_JHP')
DefineClass.JAZZ_AMMO_9x18_JHP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18JHP.png",
	DisplayName = T(865245516789, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_JHP DisplayName]] "9x18мм, СП7 JHP+"),
	DisplayNamePlural = T(360885048478, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_JHP DisplayNamePlural]] "9x18мм, СП7 JHP+"),
	colorStyle = "AmmoJHPPColor",
	Description = T(285060449915, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_JHP Description]] "Экспансивный спец патрон, бесполезен против брони, зато по мягким тканям отрабатывает не хуже старших братьев, все равно что выстрелить в человека из дробовика."),
	Cost = 600,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 10,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1400,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 120,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 40,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
}

