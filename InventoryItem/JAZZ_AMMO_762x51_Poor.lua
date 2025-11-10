UndefineClass('JAZZ_AMMO_762x51_Poor')
DefineClass.JAZZ_AMMO_762x51_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/762NATOSub.png",
	DisplayName = T(816293484485, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor DisplayName]] "7.62х51мм НАТО, FMJ Substandard"),
	DisplayNamePlural = T(784212637278, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor DisplayNamePlural]] "7.62х51мм НАТО, FMJ Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(868039456416, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor Description]] "Африканский патрон калибра 7.62х51мм НАТО"),
	AdditionalHint = T(318739847122, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_762x51_Poor AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны низкого качества: пониженный урон, увеличенный износ"),
	Cost = 660,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 30,
	CategoryPair = "762NATO",
	ShopStackSize = 20,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_762x51",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 2000,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -5,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 100,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -3,
			target_prop = "Recoil",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

