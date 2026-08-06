UndefineClass('JAZZ_AMMO_12gauge_APSlug')
DefineClass.JAZZ_AMMO_12gauge_APSlug = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Пуля ББ - 1 шт",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gAPSLUG.png",
	DisplayName = T(900455292533, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug DisplayName]] "12-й калибр, ББ Пуля"),
	DisplayNamePlural = T(527580122468, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug DisplayNamePlural]] "12-й калибр, ББ Пуля"),
	colorStyle = "AmmoAPColor",
	Description = T(476217082330, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_APSlug Description]] "Боеприпас на случай важных переговоров, вдруг вы хотите охотиться не на живые организмы, а скажем, сбить гражданский вертолёт или остановить грузовик?"),
	AdditionalHint = "",
	Cost = 1800,
	CanAppearInShop = true,
	Tier = 4,
	MaxStock = 3,
	RestockWeight = 14,
	ShopStackSize = 25,
	MaxStacks = 20,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "OverwatchAngle",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 15,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 38,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 500,
			target_prop = "ObjDamageMod",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 980,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 9,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 20,
			target_prop = "BaseJamChance",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_ap.png",
}

