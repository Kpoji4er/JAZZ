UndefineClass('JAZZ_AMMO_762x51_Match')
DefineClass.JAZZ_AMMO_762x51_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOM118.png",
	DisplayName = T(378844614691, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Match DisplayName]] "7.62х51мм НАТО, M118LR"),
	DisplayNamePlural = T(218380185132, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Match DisplayNamePlural]] "7.62х51мм НАТО, M118LR"),
	colorStyle = "AmmoMatchColor",
	Description = T(289283680399, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Match Description]] "Специальный снайперский армейский патрон M118LR калибра 7.62х51мм НАТО"),
	AdditionalHint = T(603517978310, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Match AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 6000,
	CanAppearInShop = true,
	Tier = "5",
	MaxStock = 5,
	RestockWeight = 3,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 3000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
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
			mod_add = 6,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "CritChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

