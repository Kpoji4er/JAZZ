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
	DisplayName = T(279226942480, "Под огнем"),
	Description = T(880250024564, "Шанс попасть во врага снижен\n+1 ОД свободного перемещения"),
	AddEffectText = T(551437047571, "Под плотным огнем"),
	OnAdded = function (self, obj)
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "TacticalRevenge")
		                    else
		                        PlayVoiceResponse(obj, "TacticalTaunt")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/suppressionMedium.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

