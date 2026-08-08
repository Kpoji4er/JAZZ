UndefineClass('Jazz_MiguelAuraUp')
DefineClass.Jazz_MiguelAuraUp = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "cth_bonus",
			'Value', 15,
			'Tag', "<cth_bonus>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "will_bonus",
			'Value', 30,
			'Tag', "<will_bonus>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				ApplyCthModifier_Add(self, data, self:ResolveValue("cth_bonus") or 15)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "StatusEffectAdded",
			Handler = function (self, target, id)
				if id ~= self.class then
					return
				end
				if type(target.WillPoints) == "number" and type(target.MaxWillPoints) == "number" then
					target.WillPoints = Min(target.MaxWillPoints, target.WillPoints + (self:ResolveValue("will_bonus") or 30))
				end
			end,
		}),
	},
	DisplayName = T(890000000009895, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraUp DisplayName]] "Команданте (+)"),
	Description = T(890000000009896, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraUp Description]] "+15 CTH и +30 Will, пока Мигель в ауре и на ногах."),
	Icon = "UI/Hud/Status effects/accuracy",
	type = "Buff",
	lifetime = "Until End of Turn",
	RemoveOnEndCombat = true,
	Shown = true,
}
