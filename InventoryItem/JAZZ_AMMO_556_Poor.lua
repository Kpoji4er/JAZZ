UndefineClass('JAZZ_AMMO_556_Poor')
DefineClass.JAZZ_AMMO_556_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556Sub.png",
	DisplayName = T(890000000000737, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor DisplayName]] "5,56мм, .223 Rem Commercial Substandard"),
	DisplayNamePlural = T(890000000001036, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor DisplayNamePlural]] "5,56 мм, .223 Rem Commercial Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000001054, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor Description]] "Можно сказать что это коммерческий патрон калибра 5.56, на деле же это не выдающийся охотничий .223, нет даже уверенности, что в нем хватит мощности для автоматической стрельбы."),
	AdditionalHint = "",
	Cost = 400,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 3,
	RestockWeight = 90,
	CategoryPair = "556",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_556",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 70,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
}

