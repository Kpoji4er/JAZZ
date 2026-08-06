UndefineClass('suppressionPinned')
DefineClass.suppressionPinned = {
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
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local ap = target.ActionPoints
				target.ActionPoints = Clamp(target.ActionPoints, 0, 4*const.Scale.AP)
				target:RemoveStatusEffect("FreeMove")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcPersonalMorale",
			Handler = function (self, target, value)
				return value - 1
			end,
		}),
	},
	DisplayName = T(890000000000262, --[[ModItemCharacterEffectCompositeDef suppressionPinned DisplayName]] "Прижат"),
	Description = T(890000000001235, --[[ModItemCharacterEffectCompositeDef suppressionPinned Description]] "Количество ОД — не более 4.\nНе может контратаковать или поддерживать подготовленные атаки."),
	AddEffectText = T(890000000000704, --[[ModItemCharacterEffectCompositeDef suppressionPinned AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		obj:InterruptPreparedAttack()
		local unitStance = obj.stance
		if unitStance ~= "Prone" or not (obj:CanTakeCover()) then
		obj:SetActionCommand("ChangeStance", nil, nil, "Prone")
		end
		if obj:CanTakeCover() then
		obj:TakeCover();
		obj:SetActionCommand("TakeCover", nil, nil, "Prone")
		end
		
		obj.ActionPoints = Clamp(obj.ActionPoints, 0, 4*const.Scale.AP)
		
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "AIArchetypeScared")
		                    else
		                        PlayVoiceResponse(obj, "AILoseCover")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/suppressionPinned.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

