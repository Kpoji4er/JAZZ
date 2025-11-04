UndefineClass('Slowed')
DefineClass.Slowed = {
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
					patient:RemoveStatusEffect("Slowed")
				end
				end
			end,
			HandlerCode = function (self, patient, hp, medkit, healer)
				if SkillCheck(healer, "Medical", 50) then
					patient:RemoveStatusEffect("Slowed")
				end
			end,
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function (self, target, value, action)
				return value + self:ResolveValue("move_ap_modifier")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local effect = target:GetStatusEffect("Wounded")
				local count = 0
				if effect then
				 	count = effect.stacks 
				end
				local mod = count * 10
				
				local hp = target.TempHitPoints + target.HitPoints
				if target:Random(hp) > 50   then
					target:RemoveStatusEffect("Slowed")
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
	DisplayName = T(816046468188, "Замедление"),
	Description = T(298835539293, "<color EmStyle>Стоимость перемещения</color> повышена на <color EmStyle><move_ap_modifier>%</color> за уровень.\nИмеет шанс вылечиться со временем после лечения или при высоком здоровье"),
	AddEffectText = T(501562259156, "<color EmStyle><DisplayName></color> в состоянии замедления"),
	OnAdded = function (self, obj)
		Msg("UnitAPChanged", obj)
	end,
	OnRemoved = function (self, obj)
		Msg("UnitAPChanged", obj)
	end,
	type = "Debuff",
	Icon = "UI/Hud/Status effects/legs_pain",
	max_stacks = 2,
	Shown = true,
	HasFloatingText = true,
}

