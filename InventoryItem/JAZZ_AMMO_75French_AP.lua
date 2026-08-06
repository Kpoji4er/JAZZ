UndefineClass('JAZZ_AMMO_75French_AP')
DefineClass.JAZZ_AMMO_75French_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/75AP.png",
	DisplayName = T(890000000000134, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP DisplayName]] "7,5х54 мм, Balle P (AP)"),
	DisplayNamePlural = T(890000000001059, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP DisplayNamePlural]] "7,5х54 мм, Balle P (AP)"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000827, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP Description]] "Бронебойные патроны, действительно суровые и эффективные, можно не только прошибать броню, но ещё и броню за стенами."),
	Cost = 850,
	CanAppearInShop = false,
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "792",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_75French",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
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
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
	},
}

