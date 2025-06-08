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
				target.ActionPoints = Min(4,ap)
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
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef suppressionPinned DisplayName]] "Прижат"),
	Description = T(880250024564, --[[ModItemCharacterEffectCompositeDef suppressionPinned Description]] "Количество од - не более 4."),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef suppressionPinned AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		local unitStance = obj.stance
		if unitStance ~= "Prone" or not (obj:CanTakeCover()) then
		obj:SetActionCommand("ChangeStance", nil, nil, "Prone")
		end
		if obj:CanTakeCover() then
		obj:TakeCover();
		--obj:SetActionCommand("TakeCover", nil, nil, "Prone")
		end
		
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

