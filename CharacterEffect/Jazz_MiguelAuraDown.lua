UndefineClass('Jazz_MiguelAuraDown')
DefineClass.Jazz_MiguelAuraDown = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "StatusEffect",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "cth_penalty",
			'Value', 15,
			'Tag', "<cth_penalty>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "will_penalty",
			'Value', 30,
			'Tag', "<will_penalty>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				ApplyCthModifier_Add(self, data, -(self:ResolveValue("cth_penalty") or 15))
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "StatusEffectAdded",
			Handler = function (self, target, id)
				if id ~= self.class then
					return
				end
				if type(target.WillPoints) == "number" then
					target.WillPoints = Max(0, target.WillPoints - (self:ResolveValue("will_penalty") or 30))
				end
			end,
		}),
	},
	DisplayName = T(890000000009897, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraDown DisplayName]] "Команданте (−)"),
	Description = T(890000000009898, --[[ModItemCharacterEffectCompositeDef Jazz_MiguelAuraDown Description]] "−15 CTH и −30 Will, пока Мигель сбит в ауре."),
	Icon = "UI/Hud/Status effects/injured",
	type = "Debuff",
	lifetime = "Until End of Turn",
	RemoveOnEndCombat = true,
	Shown = true,
}
