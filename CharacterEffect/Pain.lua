UndefineClass('Pain')
DefineClass.Pain = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function(self, target, value)
				if not target:HasStatusEffect("Analgesia") then
					return value - self.stacks * self:ResolveValue("APLoss") * const.Scale.AP
				end
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
	DisplayName = T(890000000009202, "Pain"),
	Description = T(890000000009203, "Each stack costs <color EmStyle><APLoss> AP</color> and <color EmStyle><cth_penalty>% chance to hit</color>. Decreases by one stack each turn. Analgesia suppresses the penalties."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Pain.png",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
}
