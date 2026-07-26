UndefineClass('JAZZ_AMMO_9x19_AP')
DefineClass.JAZZ_AMMO_9x19_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/919AP.png",
	DisplayName = T(890000000000578, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP DisplayName]] "9х19 мм, 7н21 ББ"),
	DisplayNamePlural = T(890000000001378, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP DisplayNamePlural]] "9х19 мм, 7н21 ББ"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000598, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_9x19_AP Description]] "Бронебойные патроны 9х19, наконец-то можно прострелить фанерную переборку, кусок шифера и (чем не шутит черт) сможете пробить вражескую каску. Отдача усилена соответственно."),
	AdditionalHint = "",
	Cost = 900,
	CanAppearInShop = true,
	MaxStock = 20,
	RestockWeight = 10,
	CategoryPair = "9mm",
	ShopStackSize = 50,
	MaxStacks = 120,
	Caliber = "JAZZ_Caliber_9x19",
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
			mod_add = -3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 970,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

