UndefineClass('JAZZ_AMMO_792_AP')
DefineClass.JAZZ_AMMO_792_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/792x57AP.png",
	DisplayName = T(890000000000136, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_AP DisplayName]] "7,92х57 мм, SmK (ББ)"),
	DisplayNamePlural = T(890000000001061, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_AP DisplayNamePlural]] "7,92х57 мм, SmK (ББ)"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000826, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_792_AP Description]] "Бронебойная версия армейского патрона, не понятно что потребовало его изобрести, но вероятно вы рады, что у вас есть такая опция."),
	AdditionalHint = "",
	Cost = 850,
	CanAppearInShop = false,
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
			mod_add = 3,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
}

