UndefineClass('BleedingOut')
DefineClass.BleedingOut = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				if not IsInCombat() then return end
				if not RollSkillCheck(target, "Health", nil, target.downed_check_penalty) then
					--CombatLog("important", T{290150299208, "<em><LogName></em> has <em>bled out</em>", target})
					target:TakeDirectDamage(8)
				else
					target.downed_check_penalty = target.downed_check_penalty + self:ResolveValue("add_penalty")
					CombatLog("short", T{333799512710, "<em><LogName></em> is <em>bleeding</em>", target})
				end
				
				CombatBadgeAboveNameTextUpdate(target.ui_badge.idAboveName)
			end,
		}),
	},
	Conditions = {
		PlaceObj('CombatIsActive', {}),
	},
	DisplayName = T(216716472184, --[[ModItemCharacterEffectCompositeDef BleedingOut DisplayName]] "Тяжелое ранение"),
	Description = T(910957860179, --[[ModItemCharacterEffectCompositeDef BleedingOut Description]] "Этот персонаж находится в <color EmStyle>критическом состоянии</color> и истечет кровью, если его не <color EmStyle>перевязать</color>. Каждый ход персонаж будет терять 8 единиц здоровья."),
	OnAdded = function (self, obj)  end,
	Icon = "UI/Hud/Status effects/bleedingout",
	Shown = true,
}

