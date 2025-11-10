UndefineClass('JAZZ_AMMO_50BMG_APIT')
DefineClass.JAZZ_AMMO_50BMG_APIT = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "UI/Icons/Items/50bmg_incendiary",
	DisplayName = T(123694025099, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_APIT DisplayName]] ".50, ЗЖ"),
	DisplayNamePlural = T(441685737224, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_APIT DisplayNamePlural]] ".50, ЗЖ"),
	colorStyle = "AmmoTracerColor",
	Description = T(676306531266, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_APIT Description]] "Зажигательный боеприпас для пулеметов, снайперских винтовок, пистолетов и револьверов калибра .50."),
	AdditionalHint = T(436470927890, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_50BMG_APIT AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>горение</color>"),
	Cost = 72000,
	CanAppearInShop = true,
	Tier = "5",
	MaxStock = 5,
	RestockWeight = 1,
	CategoryPair = "50BMG",
	ShopStackSize = 5,
	Caliber = "JAZZ_Caliber_50BMG",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 4000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 200,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "Recoil",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 6,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 30,
			target_prop = "CritChance",
		}),
	},
	AppliedEffects = {
		"Exposed",
		"Burning",
	},
	ammo_type_icon = "UI/Icons/Items/ta_shock.png",
}

