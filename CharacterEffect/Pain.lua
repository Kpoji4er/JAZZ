UndefineClass('Pain')
DefineClass.Pain = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "APLoss",
			'Value', 1,
			'Tag', "<APLoss>",
		}),
		PlaceObj('PresetParamPercent', {
			'Name', "cth_penalty",
			'Value', 5,
			'Tag', "<cth_penalty>%",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				local penalty = self.stacks * self:ResolveValue("APLoss") * const.Scale.AP
				if target:HasStatusEffect("Analgesia") then
					self:SetParameter("jazz_ap_penalty_applied", 0)
					self:SetParameter("jazz_ap_penalty_turn", -1)
					return value
				end
				local applied = Min(Max(0, value), Max(0, penalty))
				self:SetParameter("jazz_ap_penalty_applied", applied)
				self:SetParameter("jazz_ap_penalty_turn", (rawget(_G, "g_Combat") and g_Combat.current_turn) or -1)
				return value - penalty
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker and not attacker:HasStatusEffect("Analgesia") then
					ApplyCthModifier_Add(self, data, -self.stacks * self:ResolveValue("cth_penalty"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				target:RemoveStatusEffect("Pain", 1)
			end,
		}),
	},
	DisplayName = T(890000000010007, "Pain"),
	Description = T(890000000010008, "Each stack costs <color EmStyle><APLoss> AP</color> and <color EmStyle><cth_penalty>% chance to hit</color>. Decreases by one stack each turn. Clears when combat ends. Morphine clears Pain and blocks new stacks while Analgesia lasts."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Pain.png",
	max_stacks = 8,
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}
