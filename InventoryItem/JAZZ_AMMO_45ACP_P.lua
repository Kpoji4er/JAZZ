UndefineClass('JAZZ_AMMO_45ACP_P')
DefineClass.JAZZ_AMMO_45ACP_P = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPP.png",
	DisplayName = T(911933649700, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P DisplayName]] ".45ACP, +P"),
	DisplayNamePlural = T(399199708303, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P DisplayNamePlural]] ".45ACP, +P"),
	colorStyle = "AmmoHPColor",
	Description = T(191747956366, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_P Description]] "Попытка добавить базовому патрону бронебойности не изменяя конструкции пули, и это удалось, теперь владельцы базовой защиты могут трепетать. Имеются побочные эффекты, однако оно того стоит."),
	AdditionalHint = "",
	Cost = 540,
	CanAppearInShop = true,
	Tier = 1,
	MaxStock = 8,
	RestockWeight = 80,
	CategoryPair = "45ACP",
	ShopStackSize = 50,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -6,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 60,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 960,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 18,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

