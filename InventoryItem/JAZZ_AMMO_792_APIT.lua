UndefineClass('JAZZ_AMMO_792_APIT')
DefineClass.JAZZ_AMMO_792_APIT = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/792x57API.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT DisplayName]] "7,92х57 мм, SmK L'spur (API-T)"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT DisplayNamePlural]] "7,92х57 мм, SmK L'spur (API-T)"),
	colorStyle = "AmmoAPPColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_APIT Description]] "Комбинированный бронебойный трассер - даёт и пробитие, и визуальную трассу для корректировки огня."),
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

