UndefineClass('suppressionMedium')
DefineClass.suppressionMedium = {
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
				target:GainAP(1, "Move")
			end,
		}),
	},
	DisplayName = T(890000000000260, --[[ModItemCharacterEffectCompositeDef suppressionMedium DisplayName]] "Под огнем"),
	Description = T(890000000001238, --[[ModItemCharacterEffectCompositeDef suppressionMedium Description]] "Шанс попасть во врага снижен\n+1 ОД свободного перемещения"),
	AddEffectText = T(890000000000704, --[[ModItemCharacterEffectCompositeDef suppressionMedium AddEffectText]] "Под плотным огнем"),
	OnAdded = function (self, obj)
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "TacticalRevenge")
		                    else
		                        PlayVoiceResponse(obj, "TacticalTaunt")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/suppressionMedium.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

