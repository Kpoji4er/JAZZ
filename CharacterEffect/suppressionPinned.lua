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
	DisplayName = T(279226942480, "Прижат"),
	Description = T(880250024564, "Количество од - не более 4."),
	AddEffectText = T(551437047571, "Под плотным огнем"),
	OnAdded = function (self, obj)
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
	Icon = "Mod/e6L4ECj/Icons/suppressionPinned.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

