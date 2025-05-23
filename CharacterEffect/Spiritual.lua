UndefineClass('Spiritual')
DefineClass.Spiritual = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attacker then
					data.min = self:ResolveValue("minAccuracy")
				end
			end,
		}),
	},
	DisplayName = T(906477417382, --[[ModItemCharacterEffectCompositeDef Spiritual DisplayName]] "Духовность"),
	Description = T(233455514627, --[[ModItemCharacterEffectCompositeDef Spiritual Description]] "Гарантированная <em>минимальная точность</em> для безнадежных атак."),
	Icon = "UI/Icons/Perks/Spiritual",
	Tier = "Quirk",
}

