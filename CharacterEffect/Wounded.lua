UndefineClass('Wounded')
DefineClass.Wounded = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {
		PlaceObj('MsgActorReaction', {
			ActorParam = "attacker",
			Event = "GatherCTHModifications",
			Handler = function (self, attacker, cth_id, action_id, target, weapon1, weapon2, data)
				local reaction_def = (self.msg_reactions or empty_table)[1]
				if self:VerifyReaction("GatherCTHModifications", reaction_def, attacker, attacker, cth_id, action_id, target, weapon1, weapon2, data) then
					-----------------
				local effect = attacker:GetStatusEffect("Wounded")
				local count = 0
				if effect then
				 	count = effect.stacks 
				end
				--if cth_id == self.id then
				--	data.mod_add = data.mod_add + self:ResolveValue("cth_penalty")*count
				--end
				---------------
				end
			end,
			HandlerCode = function (self, attacker, cth_id, action_id, target, weapon1, weapon2, data)
				-----------------
				local effect = attacker:GetStatusEffect("Wounded")
				local count = 0
				if effect then
				 	count = effect.stacks 
				end
				--if cth_id == self.id then
				--	data.mod_add = data.mod_add + self:ResolveValue("cth_penalty")*count
				--end
				---------------
			end,
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnStatusEffectAdded",
			Handler = function (self, target, id, stacks)
				if self.class == id then
					-- handle add/remove stacks
					RecalcMaxHitPoints(target)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnStatusEffectRemoved",
			Handler = function (self, target, id, stacks_remaining)
				if self.class == id and stacks_remaining > 0 then
					-- handle add/remove stacks
					RecalcMaxHitPoints(target)	
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcStartTurnAP",
			Handler = function (self, target, value)
				----------------------------
				local effect = target:GetStatusEffect("Wounded", "all")
				local count = 0
				if effect then
				 	count = effect.stacks 
					--print(effect.stacks)
				end
					local ap_loss = (-count * const.Scale.AP)
					value = value - ap_loss
					
				
				--------------------------------
			end,
		}),
	},
	DisplayName = T(738668654416, --[[ModItemCharacterEffectCompositeDef Wounded DisplayName]] "Ранен"),
	Description = T(345786294171, --[[ModItemCharacterEffectCompositeDef Wounded Description]] "Макс. количество <color EmStyle>ОЗ снижается на <MaxHpReductionPerStack></color> за каждую рану. Так же с каждой раной снижается <color EmStyle>Количество ОД </color>. Можно вылечить операцией <color EmStyle>Лечение ран</color> в режиме Вида со спутника."),
	OnAdded = function (self, obj)
		RecalcMaxHitPoints(obj)
		
		if not IsKindOf(obj, "Unit") then
			return
		end
		---------------------------------------
		local effect = obj:GetStatusEffect("Wounded")
		local count
		if effect then
		 	count = effect.stacks 
		else 
			count = 0
		end
		local mod1 = 20 + count * (-10)
		
		if not RollSkillCheck(obj, "Health", 90, mod1) then
			obj:AddStatusEffect("Bleeding")
		end
		
		--if not RollSkillCheck(obj, "Health", 70, mod1) then
		--	obj:AddStatusEffect("Bleeding")
		--end
		
		--if not RollSkillCheck(obj, "Health", 50, mod1) then
		--	local roll = 1 + obj:Random(100)
		--	if roll < 35 then
		--	obj:AddStatusEffect("Slowed")
		--	elseif roll <70 then
		--	obj:AddStatusEffect("Inaccurate")
		--	elseif roll <85 then
		--	obj:AddStatusEffect("Blinded")
		--	else
		--	obj:AddStatusEffect("Unconscious")
		--	end 	
		--end
		
		---------------------------------------------------------------
		
		if not obj:HasStainType("Blood") then
			local spot = obj:GetEffectValue("wounded_stain_spot")
			if spot then
				obj:AddStain("Blood", spot)
			end
		end
		
		if not obj.wounded_this_turn and GameState.Heat then
			if not RollSkillCheck(obj, "Health") then
				obj:ChangeTired(1)
			end
		end
		local attackObj = obj.hit_this_turn and obj.hit_this_turn[#obj.hit_this_turn]
		local friendlyFire = attackObj and attackObj.team and obj.team and attackObj.team :IsAllySide(obj.team)
		local effect = obj:GetStatusEffect("Wounded")
		if effect.stacks >= 4 and obj:IsMerc() and not friendlyFire then
			PlayVoiceResponse(obj, "SeriouslyWounded")
		elseif not friendlyFire then
			PlayVoiceResponse(obj, "Wounded")
		end
		obj.wounded_this_turn = true
	end,
	OnRemoved = function (self, obj)
		RecalcMaxHitPoints(obj)
		if obj:IsKindOf("Unit") and not obj:IsDead() then
			obj:ClearStains("Blood")
		end
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/wounded",
	max_stacks = 999,
	dontRemoveOnDeath = true,
	Shown = true,
	ShownSatelliteView = true,
}

