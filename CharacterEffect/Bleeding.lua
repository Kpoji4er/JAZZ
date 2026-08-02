UndefineClass('Bleeding')
DefineClass.Bleeding = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function(self, target)
				JazzBleedOnUnitEndTurn(target)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function(self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					ApplyCthModifier_Add(self, data, self:ResolveValue("cth_penalty") * self.stacks)
				end
			end,
		}),
	},
	DisplayName = T(779855732255, "Bleeding"),
	Description = T(890000000009195, "Light bleeding: <color EmStyle><DamagePerTurn> HP</color> per stack each turn. Bandage removes one light stack (or reduces a worse stack by one tier)."),
	AddEffectText = T(488938284982, "<color EmStyle><DisplayName></color> is bleeding"),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Bleeding.png",
	max_stacks = 8,
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
