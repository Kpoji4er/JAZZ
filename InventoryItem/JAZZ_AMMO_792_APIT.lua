UndefineClass('JAZZ_AMMO_792_APIT')
DefineClass.JAZZ_AMMO_792_APIT = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/792x57API.png",
	DisplayName = T(890000000000137, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT DisplayName]] "7,92х57 мм, SmK L'spur (API-T)"),
	DisplayNamePlural = T(890000000001062, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT DisplayNamePlural]] "7,92х57 мм, SmK L'spur (API-T)"),
	colorStyle = "AmmoAPPColor",
	Description = T(890000000000825, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT Description]] "БЗТ патрон, что ещё тут надо добавлять? Он прекрасен, хоть и стар. Превратите войну в искусство."),
	AdditionalHint = "",
	Cost = 1440,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "792",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_792",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
}

