UndefineClass('AutoWeapons')
DefineClass.AutoWeapons = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if id == "Autofire" and target == attacker then
					data.mod_mul = AutoWeapons:ResolveValue("automatics_penalty_reduction")
					data.meta_text[#data.meta_text+1] = T{776394275735, "Perk: <name>", name = self.DisplayName}
				end
			end,
		}),
	},
	DisplayName = T(971350457853, --[[ModItemCharacterEffectCompositeDef AutoWeapons DisplayName]] "Auto Weapons"),
	Description = T(253479657834, --[[ModItemCharacterEffectCompositeDef AutoWeapons Description]] "Увеличивает количество выстрелов без отдачи на 1 при стрельбе очередями или в автоогне"),
	Icon = "UI/Icons/Perks/AutoWeapons",
	Tier = "Specialization",
}

