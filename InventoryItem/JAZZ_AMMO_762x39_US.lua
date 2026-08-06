UndefineClass('JAZZ_AMMO_762x39_US')
DefineClass.JAZZ_AMMO_762x39_US = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	RepairCost = 200,
	Icon = "Mod/e6L4ECj/Ammopics/762x39SS.png",
	DisplayName = T(343683428790, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US DisplayName]] "7,62х39мм, УС"),
	DisplayNamePlural = T(586453294366, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US DisplayNamePlural]] "7,62х39мм, УС"),
	colorStyle = "AmmoSubsonicColor",
	Description = T(317343617056, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US Description]] "Бесполезный пережиток бесшумных комплексов, летит не далеко, не быстро, враг может даже не заметить, что в него стреляли."),
	Cost = 500,
	CanAppearInShop = true,
	Tier = 1,
	RestockWeight = 100,
	MaxStock = 8,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 990,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -20,
			target_prop = "Noise",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

