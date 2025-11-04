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
				--if not IsInCombat() then return end
				if target:HasStatusEffect("BeingBandaged") then
					target:RemoveStatusEffect("Bleeding", "all")
					return
				end
				-----------------------------------
				local effect = target:GetStatusEffect("Bleeding", "all")
				local count = 0
				if effect then
				 	count = effect.stacks 
					--print(effect)
				end
				local value = self:ResolveValue("DamagePerTurn") * count
				--value = target:Random(value)
				--print(value)
				----------------------------------------------------
				
				local floating_text = T{193053798048, "<num> (кровотечение)", num = value}
				local pov_team = GetPoVTeam()
				local has_visibility = HasVisibilityTo(pov_team, target)
				local log_msg = T{729241506274, "<name> получает <em>урон в <num> </em> из-за кровотечения", name = target:GetLogName(), num = value}
				target:TakeDirectDamage(value, has_visibility and floating_text or false, "short", log_msg)
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
		PlaceObj('UnitReaction', {
			Event = "OnUnitBandaged",
			Handler = function (self, target, healer, patient, hp_restored)
				if target == patient then
					target:RemoveStatusEffect(self.class)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				----------------------------
				local effect = target:GetStatusEffect("Bleeding", "all")
				local count = 0
				if effect then
				 	count = effect.stacks 
					--print(effect.stacks)
				end
				if count == 3 then
				
					local ap_loss = (-self:ResolveValue("APLoss") * const.Scale.AP)
					value = value - ap_loss
					
				end
				--------------------------------
			end,
		}),
	},
	DisplayName = T(425969373535, "Кровотечение"),
	Description = T(326849165819, "Этот боец каждый ход будет <color EmStyle>получать урон до <DamagePerTurn> ОЗ</color> за уровень кровотечения до тех пор пока не будет <color EmStyle>перевязан</color>. При третьем уровне кровотечения макс. количество <color EmStyle>ОД будет снижено на <APLoss></color>."),
	AddEffectText = T(488938284982, "<color EmStyle><DisplayName></color> истекает кровью"),
	OnAdded = function (self, obj)
		if g_Teams[g_CurrentTeam] == obj.team and not obj:HasStatusEffect("BeingBandaged") then
		-------------------
		   local effect = obj:GetStatusEffect("Bleeding", "all")
			local count = 0
			if effect then
			 	count = effect.stacks 
			end
		    if count == 3 then
		--------------------------------------''
				obj:ConsumeAP(-self:ResolveValue("APLoss") * const.Scale.AP)
			end
		end
	end,
	OnRemoved = function (self, obj)
		--if g_Combat and not obj:HasStatusEffect("BeingBandaged") then
			--obj:ConsumeAP(self:ResolveValue("APLoss") * const.Scale.AP)
		--end
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/bleeding",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

