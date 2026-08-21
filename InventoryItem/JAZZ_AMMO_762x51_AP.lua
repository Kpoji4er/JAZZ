UndefineClass('JAZZ_AMMO_762x51_AP')
DefineClass.JAZZ_AMMO_762x51_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM61.png",
	DisplayName = T(213865838245, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_AP DisplayName]] "7.62х51мм НАТО, M61"),
	DisplayNamePlural = T(732360181829, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_AP DisplayNamePlural]] "7.62х51мм НАТО, M61"),
	colorStyle = "AmmoAPColor",
	Description = T(134217744335, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_AP Description]] "По идее должен прошибать ткань мироздания, на деле обычный бронебойный патрон, не хуже многих, вражеские каски должны трепетать, точно вам говорю, но для стрельбы из пулемета расточительно."),
	AdditionalHint = "",
	Cost = 3200,
	CanAppearInShop = true,
	Tier = 5,
	MaxStock = 2,
	RestockWeight = 8,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
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
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "Recoil",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

