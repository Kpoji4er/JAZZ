UndefineClass('Medkit')
DefineClass.Medkit = {
	__parents = { "Medicine" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Medicine",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if self == medkit then
					data.heal_modifier = data.heal_modifier + 25
				end
			end,
		}),
	},
	ScrapParts = 1,
	Repairable = false,
	Icon = "UI/Icons/Items/medkit",
	DisplayName = T(517638397088, "Аптечка"),
	DisplayNamePlural = T(532410536439, "Аптечки"),
	AdditionalHint = T(655535396072, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует состояние умирающих персонажей\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Требуется для использования перевязки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Перевязка восстанавливает на 25% ОЗ больше\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Тратится при каждом употреблении, но запас медикаментов можно восполнить\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Medical",
	Cost = 500,
	CanAppearInShop = true,
	Tier = 2,
	CategoryPair = "Medicine",
	max_meds_parts = 12,
	UsePriority = 1,
}

