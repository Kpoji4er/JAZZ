UndefineClass('BuildingConfidence')
DefineClass.BuildingConfidence = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "percentPerLevel",
			'Value', 10,
			'Tag', "<percentPerLevel>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "percentCap",
			'Value', 50,
			'Tag', "<percentCap>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not g_Combat then
					return
				end
				-- Turn 2, then every 3 turns after: 2, 5, 8, 11…
				local turn = g_Combat.current_turn or 1
				if turn >= 2 and ((turn - 2) % 3 == 0) then
					target:AddStatusEffect("Inspired")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if target ~= medic or not data or not patient then
					return
				end
				local apply = rawget(_G, "Jazz_BuildingConfidenceApplyHealMod")
				if type(apply) == "function" then
					apply(medic, patient, data)
					return
				end
				local per = self:ResolveValue("percentPerLevel") or 10
				local cap = self:ResolveValue("percentCap") or 50
				local medic_lvl = (medic.GetLevel and medic:GetLevel()) or 1
				local patient_lvl = (patient.GetLevel and patient:GetLevel()) or 1
				local delta = (tonumber(medic_lvl) or 1) - (tonumber(patient_lvl) or 1)
				local bonus = Clamp(delta * per, -cap, cap)
				if bonus == 0 then
					return
				end
				data.heal_modifier = MulDivRound(data.heal_modifier or 100, 100 + bonus, 100)
			end,
		}),
	},
	DisplayName = T(890000000009877, --[[ModItemCharacterEffectCompositeDef BuildingConfidence DisplayName]] "Уверенность растёт"),
	Description = T(890000000009878, --[[ModItemCharacterEffectCompositeDef BuildingConfidence Description]] "На 2-м ходу и каждые 3 хода после (2/5/8…) — Inspired (+4 ОД). Лечение: ±<percentPerLevel>% за разницу уровней с пациентом (макс. ±<percentCap>%), в бою и на спутнике."),
	Icon = "UI/Icons/Perks/BuildingConfidence",
	Tier = "Personal",
}
