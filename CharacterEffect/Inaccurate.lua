UndefineClass('Inaccurate')
DefineClass.Inaccurate = {
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
					if SkillCheck(healer, "Medical", 50) then
					patient:RemoveStatusEffect("Inaccurate")
				end
				end
			end,
			HandlerCode = function (self, patient, hp, medkit, healer)
				if SkillCheck(healer, "Medical", 50) then
					patient:RemoveStatusEffect("Inaccurate")
				end
			end,
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				local effect = target:GetStatusEffect("Inaccurate")
				local count = 1
												if effect then
												 	count = effect.stacks 
												end
				
				if target == attacker then
					ApplyCthModifier_Add(self, data, count * self:ResolveValue("accuracy_modifier"))
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local hp = target.TempHitPoints + target.HitPoints
				if target:Random(hp) > 50   then
					target:RemoveStatusEffect("Inaccurate")
					end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnNewHour",
			Handler = function (self, target)
				local effect = target:GetStatusEffect("Wounded")
				local count
				if effect then
				 	count = effect.stacks 
				else 
					count = 0
				end
				
				if count<3 then 
					target:RemoveStatusEffect("Slowed")
				end
			end,
		}),
	},
	DisplayName = T(260481671641, --[[ModItemCharacterEffectCompositeDef Inaccurate DisplayName]] "Inaccurate"),
	Description = T(538313284813, --[[ModItemCharacterEffectCompositeDef Inaccurate Description]] "Значительный <color EmStyle>штраф к точности</color> для всех атак. \nИмеет шанс вылечиться со временем после лечения или при высоком здоровье"),
	type = "Debuff",
	Icon = "UI/Hud/Status effects/arms_pain",
	max_stacks = 2,
	Shown = true,
	HasFloatingText = true,
}

