UndefineClass('JAZZ_AMMO_3006_Match')
DefineClass.JAZZ_AMMO_3006_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "30-06",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/3006Match.png",
	DisplayName = T(697162729896, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_Match DisplayName]] "Патрон 30-06 M25 Match"),
	DisplayNamePlural = T(726631612816, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_Match DisplayNamePlural]] "Патроны 30-06 M25 Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(898567748151, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_3006_Match Description]] "Высокоточный патрон, помимо прочего имеет хорошее пробитие и какую-никакую экспансивность, какой-то новодел, но мы ничего против не имеем, убивать надо эффективно."),
	Cost = 840,
	CanAppearInShop = true,
	MaxStock = 30,
	RestockWeight = 1,
	CategoryPair = "3006",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_3006",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 8,
			target_prop = "CritChance",
		}),
	},
}

