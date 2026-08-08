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
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if target ~= medic or not data then
					return
				end
				local lvl = 1
				if medic.GetLevel then
					lvl = medic:GetLevel() or 1
				end
				local bonus = Clamp((tonumber(lvl) or 1) * 10, 0, 50)
				data.heal_modifier = MulDivRound(data.heal_modifier or 100, 100 + bonus, 100)
			end,
		}),
	},
	DisplayName = T(890000000009877, --[[ModItemCharacterEffectCompositeDef BuildingConfidence DisplayName]] "Уверенность растёт"),
	Description = T(890000000009878, --[[ModItemCharacterEffectCompositeDef BuildingConfidence Description]] "На 2-м ходу боя и каждом 3-м ходу — Inspired. Лечение ±10% за уровень (макс. ±50%) в бою и на спутнике."),
	Icon = "UI/Icons/Perks/BuildingConfidence",
	Tier = "Personal",
}
