UndefineClass('DangerClose')
DefineClass.DangerClose = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "minRange",
			'Value', 8,
			'Tag', "<minRange>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "damageBonus",
			'Value', 40,
			'Tag', "<damageBonus>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndChance",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker or not data or not IsKindOf(attack_target, "Unit") then
					return
				end
				local dist = DivRound(attacker:GetDist(attack_target), const.SlabSizeX)
				local min_r = self:ResolveValue("minRange") or 8
				if dist < min_r then
					return
				end
				local bonus = self:ResolveValue("damageBonus") or 40
				data.base_damage = MulDivRound(data.base_damage or data.damage or 0, 100 + bonus, 100)
			end,
		}),
	},
	DisplayName = T(890000000009889, --[[ModItemCharacterEffectCompositeDef DangerClose DisplayName]] "Опасная близость"),
	Description = T(890000000009890, --[[ModItemCharacterEffectCompositeDef DangerClose Description]] "По целям ≥8 клеток: +40% урона и +2 Bleeding (без штрафа стимов — soft)."),
	Icon = "UI/Icons/Perks/DangerClose",
	Tier = "Personal",
}
