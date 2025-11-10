UndefineClass('JAZZ_AMMO_3006_AP')
DefineClass.JAZZ_AMMO_3006_AP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "30-06",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/3006AP.png",
	DisplayName = T(697162729896, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_AP DisplayName]] "Патрон 30-06 M2 AP"),
	DisplayNamePlural = T(726631612816, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_AP DisplayNamePlural]] "Патроны 30-06 M2 AP"),
	colorStyle = "AmmoAPColor",
	Description = T(898567748151, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_AP Description]] "Бронебойный вариант M2 с усиленной сердцевиной для поражения лёгких укрытий и конструкций. Используется, когда требуется повышенная пробивная способность против брони или металлоконструкций; дороже и реже, чем обычный M2 Ball."),
	Cost = 1080,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 1,
	CategoryPair = "3006",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_3006",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
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
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "BulletDropRange",
		}),
	},
}

