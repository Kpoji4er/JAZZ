UndefineClass('Stealthy')
DefineClass.Stealthy = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcStealthKillChance",
			Handler = function (self, target, value, attacker, attack_target, weapon, target_spot_group, aim)
				if target == attacker then
					return value + self:ResolveValue("stealthkill")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStealthKillMinChance",
			Handler = function (self, target, value, attacker, attack_target, weapon, target_spot_group, aim)
				if target == attacker then
					return Max(value, self:ResolveValue("stealthkill_minchance"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcSightModifier",
			Handler = function (self, target, value, observer, other, step_pos, darkness)
				if target == other and target:HasStatusEffect("Hidden") then
					return value - self:ResolveValue("stealthy_detection")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				if target then 
									if not target.enemy_visual_contact and not IsMerc(target) then
										target:AddStatusEffect("Hidden")
									end
				 end
			end,
		}),
	},
	DisplayName = T(408025340126, --[[ModItemCharacterEffectCompositeDef Stealthy DisplayName]] "Stealthy"),
	Description = T(651312331230, --[[ModItemCharacterEffectCompositeDef Stealthy Description]] "Harder to spot by enemies while <GameTerm('Sneaking')>.\n\nSlightly increased chance for <GameTerm('StealthKills')>."),
	Icon = "UI/Icons/Perks/Stealthy",
	Tier = "Specialization",
}

