UndefineClass('JAZZ_AMMO_762x51_Army')
DefineClass.JAZZ_AMMO_762x51_Army = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM80.png",
	DisplayName = T(155135485934, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Army DisplayName]] "7.62х51мм НАТО, M80"),
	DisplayNamePlural = T(688496678363, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Army DisplayNamePlural]] "7.62х51мм НАТО, M80"),
	colorStyle = "AmmoArmyColor",
	Description = T(296800783973, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Army Description]] "Стандартный армейский патрон, подходит для всего оружия калибра 7.62х51, тут вам и хороший пробой и высокий урон, только не требуйте слишком многого..."),
	AdditionalHint = "",
	Cost = 500,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 50,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

