UndefineClass('JAZZ_AMMO_762x54_SNB')
DefineClass.JAZZ_AMMO_762x54_SNB = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "СНБ - Матчевые + ББ",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762x54RSNB.png",
	DisplayName = T(314555250393, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_SNB DisplayName]] "7,62x54R мм СНБ"),
	DisplayNamePlural = T(299479740054, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_SNB DisplayNamePlural]] "7,62x54R мм СНБ"),
	colorStyle = "AmmoMatchColor",
	Description = T(713481016841, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_SNB Description]] "Специальный российский винтовочный снайперский боеприпас калибра 7.62х54мм с пулей СНБ"),
	AdditionalHint = T(139833383572, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x54_SNB AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 5-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания и дальность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышенный шанс критического попадания"),
	Cost = 900,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 25,
	CategoryPair = "762x54",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x54R",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 4,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1200,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "WeaponRange",
		}),
	},
}

