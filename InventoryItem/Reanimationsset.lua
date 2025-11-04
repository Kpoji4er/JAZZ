UndefineClass('Reanimationsset')
DefineClass.Reanimationsset = {
	__parents = { "Medicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Medicine",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if self == medkit then
					data.heal_modifier = data.heal_modifier + 60
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "UI/Icons/Items/reanimationsset.png",
	DisplayName = T(656217161939, "Реаниматор"),
	DisplayNamePlural = T(779911535238, "Реаниматоры"),
	AdditionalHint = T(566246707628, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует состояние умирающих персонажей\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Требуется для использования перевязки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Перевязка восстанавливает на 60% ОЗ больше\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тратится при каждом употреблении, но запас медикаментов можно восполнить\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Medical",
	max_meds_parts = 12,
	UsePriority = 2,
}

