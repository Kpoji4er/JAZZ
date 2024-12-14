UndefineClass('JAZZ_AMMO_762x51_FMJ')
DefineClass.JAZZ_AMMO_762x51_FMJ = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "FMJ - Местные, плохого качества",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATO.png",
	DisplayName = T(816293484485, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ DisplayName]] "7.62х51мм НАТО, FMJ"),
	DisplayNamePlural = T(784212637278, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ DisplayNamePlural]] "7.62х51мм НАТО, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(868039456416, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ Description]] "Африканский патрон калибра 7.62х51мм НАТО"),
	AdditionalHint = T(318739847122, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_FMJ AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны низкого качества: пониженный урон, увеличенный износ"),
	Cost = 200,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 850,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -10,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 50,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

