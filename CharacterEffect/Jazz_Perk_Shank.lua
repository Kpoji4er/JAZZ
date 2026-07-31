UndefineClass('Jazz_Perk_Shank')
DefineClass.Jazz_Perk_Shank = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target == attack_target and action and action.ActionType == "Melee Attack" then
					ApplyCthModifier_Add(self, data, -50)
				end
			end,
		}),
	},
	DisplayName = T(890000000005007, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Shank DisplayName]] "Не трогай меня"),
	Description = T(890000000005008, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Shank Description]] "Враги в ближнем бою по Шенку получают −50 к шансу попадания."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Shank.png",
	Tier = "Personal",
}
