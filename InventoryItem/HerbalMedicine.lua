UndefineClass('HerbalMedicine')
DefineClass.HerbalMedicine = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Icon = "UI/Icons/Items/herbal_medicine",
	DisplayName = T(603680939283, --[[ModItemInventoryItemCompositeDef HerbalMedicine DisplayName]] "Herbal Medicine"),
	DisplayNamePlural = T(722930256983, --[[ModItemInventoryItemCompositeDef HerbalMedicine DisplayNamePlural]] "Herbal Medicine"),
	AdditionalHint = T(952277134603, --[[ModItemInventoryItemCompositeDef HerbalMedicine AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Укрепляет силу воли\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Непредсказуемые побочные эффекты\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Без ГМО"),
	CategoryPair = "Medicine",
	MaxStacks = 20,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitAddGrit', {}),
		PlaceObj('ChangeTiredness', {
			delta = -1,
		}),
		PlaceObj('ConditionalEffect', {
			'Conditions', {
				PlaceObj('CheckRandom', {
					Chance = 15,
				}),
			},
			'Effects', {
				PlaceObj('UnitGrantAP', {}),
			},
		}),
		PlaceObj('ConditionalEffect', {
			'Conditions', {
				PlaceObj('CheckRandom', {
					Chance = 15,
				}),
			},
			'Effects', {
				PlaceObj('UnitAddStatusEffect', {
					Status = "Berserk",
				}),
			},
		}),
	},
	action_name = T(679583097578, --[[ModItemInventoryItemCompositeDef HerbalMedicine action_name]] "APPLY"),
	destroy_item = true,
}

