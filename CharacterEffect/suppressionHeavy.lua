UndefineClass('suppressionHeavy')
DefineClass.suppressionHeavy = {
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
				target:GainAP(2, "Move")
			end,
		}),
	},
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef suppressionHeavy DisplayName]] "Под плотным огнем"),
	Description = T(880250024564, --[[ModItemCharacterEffectCompositeDef suppressionHeavy Description]] "Шанс попасть во врага снижен\n+2 ОД свободного перемещения"),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef suppressionHeavy AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		local unitStance = obj.stance
		if unitStance == "Standing" then
		obj:SetActionCommand("ChangeStance", nil, nil, "Crouch")
		end
		obj:InterruptPreparedAttack()
		
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "ThreatSelection")
		                    else
		                        PlayVoiceResponse(obj, "AILoseCover")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/suppressionHeavy.png",
	RemoveOnEndCombat = true,
	Shown = true,
	HasFloatingText = true,
}

