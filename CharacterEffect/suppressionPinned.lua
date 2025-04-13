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
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if target:CanTakeCover() then
				target:TakeCover();
				--obj:SetActionCommand("TakeCover", nil, nil, "Prone")
				end
				target:ConsumeAP(100*const.Scale.AP)
				target:ConsumeAP(100*const.Scale.AP, "Move")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcPersonalMorale",
			Handler = function (self, target, value)
				return value - 1
			end,
		}),
	},
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef suppressionPinned DisplayName]] "Прижат"),
	Description = T(880250024564, --[[ModItemCharacterEffectCompositeDef suppressionPinned Description]] "Не может выполнять действия на этом ходу"),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef suppressionPinned AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		local unitStance = obj.stance
		if unitStance ~= "Prone" and not (obj:CanTakeCover()) then
		obj:SetActionCommand("ChangeStance", nil, nil, "Prone")
		end
		if obj:CanTakeCover() then
		obj:TakeCover();
		--obj:SetActionCommand("TakeCover", nil, nil, "Prone")
		end
		
		obj:ConsumeAP(100*const.Scale.AP)
		obj:ConsumeAP(100*const.Scale.AP, "Move")
		
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
	HasFloatingText = true,
}

