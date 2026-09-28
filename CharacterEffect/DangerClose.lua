UndefineClass('DangerClose')
DefineClass.DangerClose = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStimmedTiredness",
			Handler = function (self, target, value)
				return 0
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				if id == "Stimmed" or id == "Stim" then
					data.mod_add = 0
					data.mod_mul = 100
				end
			end,
		}),
	},
	DisplayName = T(890000000009925, --[[ModItemCharacterEffectCompositeDef DangerClose DisplayName]] "Опасная дальность"),
	Description = T(890000000009926, --[[ModItemCharacterEffectCompositeDef DangerClose Description]] "Гранаты и взрывчатка на дистанции ≥<minRange> клеток: +<percent(damageBonus)> урона. Взрывы дополнительно накладывают <bleed_stacks> стака кровотечения. Нет штрафов от боевых стимуляторов."),
	Icon = "UI/Icons/Perks/DangerClose",
	Tier = "Personal",
}

