UndefineClass('GrizzlyPerk')
DefineClass.GrizzlyPerk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if action.id == self.id and target == attacker then
					data.mod_mul = AutoWeapons:ResolveValue("automatics_penalty_reduction")
					data.meta_text[#data.meta_text+1] = T{776394275735, "Perk: <name>", name = self.DisplayName}
				end
			end,
		}),
	},
	DisplayName = T(380626033173, --[[ModItemCharacterEffectCompositeDef GrizzlyPerk DisplayName]] "Рэмбо"),
	Description = T(272740235755, --[[ModItemCharacterEffectCompositeDef GrizzlyPerk Description]] "<em>Атака с помощью пулемета</em> без <em>отдачи</em>."),
	Icon = "UI/Icons/Perks/GrizzlyPerk",
	Tier = "Personal",
}

