UndefineClass('JAZZ_AMMO_762x39_Poor')
DefineClass.JAZZ_AMMO_762x39_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x39SUB.png",
	DisplayName = T(403807663771, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Poor DisplayName]] "7,62х39мм, Norinco Lot 66-3 CN Substandard"),
	DisplayNamePlural = T(578647545074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Poor DisplayNamePlural]] "7,62х39мм, Norinco Lot 66-3 CN Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(296646736495, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_Poor Description]] "Перед тем как произвести данные боеприпасы порох тщательно вымачивают в воде, а пули скатывают под языком. Не позорьтесь, китайцы никогда не делали хороших патронов."),
	Cost = 270,
	CanAppearInShop = true,
	Tier = 2,
	RestockWeight = 30,
	CategoryPair = "762WP",
	ShopStackSize = 100,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_762x39",
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
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 100,
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
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

