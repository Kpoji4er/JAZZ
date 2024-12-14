UndefineClass('JAZZ_AMMO_762x39_US')
DefineClass.JAZZ_AMMO_762x39_US = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Дозвуковые - меньше отдача и шум",
	object_class = "Ammo",
	RepairCost = 200,
	Icon = "Mod/e6L4ECj/Ammopics/762x39SS.png",
	DisplayName = T(343683428790, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US DisplayName]] "7,62х39мм, УС"),
	DisplayNamePlural = T(586453294366, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US DisplayNamePlural]] "7,62х39мм, УС"),
	colorStyle = "AmmoBasicColor",
	Description = T(317343617056, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US Description]] "Специальный советский дозвуковой патрон УС калибра 7.62х39мм"),
	AdditionalHint = T(543763221074, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x39_US AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дозвуковые: пониженный урон, уменьшенная дальность, уменьшенная точность, уменьшенная громкость выстрела, увеличенная надежность"),
	Cost = 350,
	CanAppearInShop = true,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x39",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "ObjDamageMod",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "BulletDropRange",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

