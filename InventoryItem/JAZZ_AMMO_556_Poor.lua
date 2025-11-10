UndefineClass('JAZZ_AMMO_556_Poor')
DefineClass.JAZZ_AMMO_556_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/556Sub.png",
	DisplayName = T(574593171535, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor DisplayName]] "5,56мм, .223 Rem Commercial Substandard"),
	DisplayNamePlural = T(785279043850, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor DisplayNamePlural]] "5,56 мм, .223 Rem Commercial Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(790646713962, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_556_Poor Description]] "Гражданский коммерческий патрон - универсален и массово доступен. Хорош для спортивной и охотничьей стрельбы; широко применяется в AR-платформах."),
	AdditionalHint = "",
	Cost = 750,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 5,
	RestockWeight = 30,
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
}

