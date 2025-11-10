UndefineClass('JAZZ_AMMO_545_Army')
DefineClass.JAZZ_AMMO_545_Army = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/545.png",
	DisplayName = T(827774006254, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army DisplayName]] "5,45 мм, ПС Армейский"),
	DisplayNamePlural = T(138469521759, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army DisplayNamePlural]] "5,45 мм,ПС Армейский"),
	colorStyle = "AmmoArmyColor",
	Description = T(930854241886, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army Description]] "Стандартный российский армейский патрон 7Н6 калибра 5.45x39мм"),
	AdditionalHint = T(213021415103, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_545_Army AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони"),
	Cost = 900,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 15,
	RestockWeight = 20,
	CategoryPair = "545",
	ShopStackSize = 120,
	MaxStacks = 90,
	Caliber = "JAZZ_Caliber_545",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"BleedingChance",
	},
}

