UndefineClass('Bleeding')
DefineClass.Bleeding = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {
		PlaceObj('MsgActorReaction', {
			ActorParam = "patient",
			Event = "OnHeal",
			Handler = function (self, patient, hp, medkit, healer)
				local reaction_def = (self.msg_reactions or empty_table)[1]
				if self:VerifyReaction("OnHeal", reaction_def, patient, patient, hp, medkit, healer) then
					if RollSkillCheck(healer, "Medical", 100,-10) then
					patient:RemoveStatusEffect("Bleeding", "all")
				end
				if RollSkillCheck(healer, "Medical", 100,-30) then
					patient:RemoveStatusEffect("Bleeding", "all")
				end
				
				if not IsMerc(healer) then 
				    patient:RemoveStatusEffect("Bleeding", "all")
				end
				end
			end,
			HandlerCode = function (self, patient, hp, medkit, healer)
				if RollSkillCheck(healer, "Medical", 100,-10) then
					patient:RemoveStatusEffect("Bleeding", "all")
				end
				if RollSkillCheck(healer, "Medical", 100,-30) then
					patient:RemoveStatusEffect("Bleeding", "all")
				end
				
				if not IsMerc(healer) then 
				    patient:RemoveStatusEffect("Bleeding", "all")
				end
			end,
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				JazzBleedOnUnitEndTurn(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				
				if target == attacker then
				----------------------------------
					local effect = attacker:GetStatusEffect("Bleeding", "all")
					local count = 0
					if effect then
					 	count = effect.stacks 
					end
					-----------------------
					ApplyCthModifier_Add(self, data, (self:ResolveValue("cth_penalty")*count)) ----------added count
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcCritChance",
			Handler = function (self, target, attacker, attack_target, action, weapon, data)
				if target == attack_target and IsKindOf(data.weapon, "GutHookKnife") then
					data.guaranteed_crit = true
				end
			end,
		}),
	},
	DisplayName = T(779855732255, --[[ModItemCharacterEffectCompositeDef Bleeding DisplayName]] "Bleeding"),
	Description = T(890000000010000, --[[ModItemCharacterEffectCompositeDef Bleeding Description]] "Light bleeding: <color EmStyle><DamagePerTurn> HP</color> per stack each turn. Bandage removes one light stack (or reduces a worse stack by one tier)."),
	AddEffectText = T(488938284982, --[[ModItemCharacterEffectCompositeDef Bleeding AddEffectText]] "<color EmStyle><DisplayName></color> is bleeding"),
	OnAdded = function (self, obj)
		
	end,
	OnRemoved = function (self, obj)
		--if g_Combat and not obj:HasStatusEffect("BeingBandaged") then
			--obj:ConsumeAP(self:ResolveValue("APLoss") * const.Scale.AP)
		--end
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Bleeding.png",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

