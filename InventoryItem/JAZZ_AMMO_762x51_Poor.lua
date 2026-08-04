UndefineClass('JAZZ_AMMO_762x51_Poor')
DefineClass.JAZZ_AMMO_762x51_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOSub.png",
	DisplayName = T(890000000001099, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor DisplayName]] "7.62х51мм НАТО, FMJ Substandard"),
	DisplayNamePlural = T(890000000001035, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor DisplayNamePlural]] "7.62х51мм НАТО, FMJ Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(890000000001209, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor Description]] "В эти патроны забыли насыпать порох, так что ваш автомат откатится до состояния винтовки, скажите спасибо британцам. Их кстати никто не любит."),
	AdditionalHint = "",
	Cost = 660,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 30,
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
			mod_add = -3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

