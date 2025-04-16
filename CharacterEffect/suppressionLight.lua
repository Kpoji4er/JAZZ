UndefineClass('suppressionLight')
DefineClass.suppressionLight = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target.WillPoints = target.MaxWillPoints
			end,
		}),
	},
	DisplayName = T(279226942480, --[[ModItemCharacterEffectCompositeDef suppressionLight DisplayName]] "Обстрелян"),
	Description = T(880250024564, --[[ModItemCharacterEffectCompositeDef suppressionLight Description]] "Шанс попасть во врага немного снижен"),
	AddEffectText = T(551437047571, --[[ModItemCharacterEffectCompositeDef suppressionLight AddEffectText]] "Обстрелян"),
	OnAdded = function (self, obj)
		if not obj:IsDead() then
		                    if obj:IsMerc() then
		                        PlayVoiceResponse(obj, "TacticalCareful")
		                    else
		                        PlayVoiceResponse(obj, "AITaunt")
		                    end
		                end
	end,
	Icon = "Mod/e6L4ECj/Icons/suppressionLight.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

