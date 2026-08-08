UndefineClass('BuildingConfidence')
DefineClass.BuildingConfidence = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not g_Combat then
					return
				end
				local turn = g_Combat.current_turn or 1
				if turn == 2 or (turn > 0 and turn % 3 == 0) then
					target:AddStatusEffect("Inspired")
				end
			end,
		}),
	},
	DisplayName = T(890000000009877, --[[ModItemCharacterEffectCompositeDef BuildingConfidence DisplayName]] "Уверенность растёт"),
	Description = T(890000000009878, --[[ModItemCharacterEffectCompositeDef BuildingConfidence Description]] "На 2-м ходу боя и каждом 3-м ходу — Inspired. Лечение ±10% за уровень (макс. ±50%) в бою и на спутнике."),
	Icon = "UI/Icons/Perks/BuildingConfidence",
	Tier = "Personal",
}
