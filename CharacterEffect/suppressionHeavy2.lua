UndefineClass('suppressionHeavy2')
DefineClass.suppressionHeavy2 = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	msg_reactions = {},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target.WillPoints = target.MaxWillPoints
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				target:ApplySuppressionStatus()
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcMoveModifier",
			Handler = function (self, target, value, action)
				return value + self:ResolveValue("move_ap_modifier")
			end,
		}),
	},
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef suppressionHeavy2 DisplayName]] "Подавлен"),
	Description = T(880250024564, --[[ModItemCharacterEffectCompositeDef suppressionHeavy2 Description]] "Передвижение в 2 раза дороже. Точность стрельбы сильно снижена."),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef suppressionHeavy2 AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		local unitStance = obj.stance
		if unitStance == "Standing" then
		obj:SetActionCommand("ChangeStance", nil, nil, "Crouch")
		end
		
		if unitStance == "Crouch" and not (obj:CanTakeCover()) then
		obj:SetActionCommand("ChangeStance", nil, nil, "Prone")
		end
		
		obj:InterruptPreparedAttack()
		
		local unitStance = obj.stance
		if unitStance == "Standing" then
		obj:SetActionCommand("ChangeStance", nil, nil, "Crouch")
		end
		obj:InterruptPreparedAttack()
		
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "AIArchetypeAngry")
		                    else
		                        PlayVoiceResponse(obj, "AIFlanked")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/suppressionHeavy2.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

