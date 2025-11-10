UndefineClass('JAZZ_AMMO_75French_AP')
DefineClass.JAZZ_AMMO_75French_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/75AP.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP DisplayName]] "7,5х54 мм, Balle P (AP)"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP DisplayNamePlural]] "7,5х54 мм, Balle P (AP)"),
	colorStyle = "AmmoAPColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French_AP Description]] "Бронебойный вариант для 7.5×54 - предназначен для повышения пробития при взаимодействии с бронёй и конструкциями."),
	Cost = 1080,
	CanAppearInShop = true,
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

