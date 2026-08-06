UndefineClass('JAZZ_AMMO_9x18_Poor')
DefineClass.JAZZ_AMMO_9x18_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/9x18substandart.png",
	DisplayName = T(890000000001196, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Poor DisplayName]] "9x18мм, 57-Н-181С Substandard"),
	DisplayNamePlural = T(890000000000419, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Poor DisplayNamePlural]] "9x18мм, 57-Н-181С Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000000274, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x18_Poor Description]] "Патрон для стрельбы по крысам, с первого раза может убить разве что ничего."),
	Cost = 120,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 3,
	RestockWeight = 90,
	CategoryPair = "9x18",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x18",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
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

