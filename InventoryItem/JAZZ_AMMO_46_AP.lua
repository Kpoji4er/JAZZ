UndefineClass('JAZZ_AMMO_46_AP')
DefineClass.JAZZ_AMMO_46_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/46AP.png",
	DisplayName = T(890000000000020, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_AP DisplayName]] "4,6 мм, DM11 ББ"),
	DisplayNamePlural = T(890000000000090, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_AP DisplayNamePlural]] "4,6 мм, DM11 ББ"),
	colorStyle = "AmmoAPColor",
	Description = T(890000000000574, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_46_AP Description]] "Бронебойный патрон для МП-7, Редкий боеприпас, вы либо мажор, либо счастливчик. Считайте, что стреляете золотыми слитками."),
	AdditionalHint = "",
	Cost = 1200,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 5,
	CategoryPair = "57",
	ShopStackSize = 50,
	MaxStacks = 60,
	Caliber = "JAZZ_Caliber_46",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "Recoil",
		}),
	},
}

