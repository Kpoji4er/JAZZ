UndefineClass('TagTeam')
DefineClass.TagTeam = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker then
					return
				end
				if type(Jazz_TagTeamAllyPinDown) == "function" and Jazz_TagTeamAllyPinDown(attacker, attack_target) then
					ApplyCthModifier_Add(self, data, 15)
				end
			end,
		}),
	},
	DisplayName = T(890000000009865, --[[ModItemCharacterEffectCompositeDef TagTeam DisplayName]] "Парный заход"),
	Description = T(890000000009866, --[[ModItemCharacterEffectCompositeDef TagTeam Description]] "+15% точности по целям под Pin Down союзника."),
	Icon = "UI/Icons/Perks/TagTeam",
	Tier = "Personal",
}
