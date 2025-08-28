UndefineClass('_762NATO_Match')
DefineClass._762NATO_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "M118LR - Матчевый",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(812085002897, "7.62х51мм НАТО, M118LR"),
	DisplayNamePlural = T(791984219669, "7.62х51мм НАТО, M118LR"),
	colorStyle = "AmmoMatchColor",
	Description = T(486517753713, "Специальный снайперский армейский патрон M118LR калибра 7.62х51мм НАТО"),
	AdditionalHint = T(688295270093, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 200,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 10,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762NATO",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "AimAccuracy",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "Noise",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1100,
			target_prop = "WeaponRange",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

