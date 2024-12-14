UndefineClass('_762NATO_HP')
DefineClass._762NATO_HP = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "FMJ - Местные, плохого качества",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(952380918979, --[[ModItemInventoryItemCompositeDef _762NATO_HP DisplayName]] "7.62х51мм НАТО, FMJ"),
	DisplayNamePlural = T(894698243806, --[[ModItemInventoryItemCompositeDef _762NATO_HP DisplayNamePlural]] "7.62х51мм НАТО, FMJ"),
	colorStyle = "AmmoBasicColor",
	Description = T(733817360256, --[[ModItemInventoryItemCompositeDef _762NATO_HP Description]] "Африканский патрон калибра 7.62х51мм НАТО"),
	AdditionalHint = T(224168487168, --[[ModItemInventoryItemCompositeDef _762NATO_HP AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 2-м классом брони\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Патроны низкого качества: пониженный урон, увеличенный износ"),
	Cost = 200,
	Tier = 2,
	MaxStock = 50,
	RestockWeight = 150,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762NATO",
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
			mod_add = -4,
			target_prop = "AimAccuracy",
		}),
	},
	AppliedEffects = {
		"Bleeding",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

