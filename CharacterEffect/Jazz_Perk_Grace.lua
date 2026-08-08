UndefineClass('Jazz_Perk_Grace')
DefineClass.Jazz_Perk_Grace = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker or not data or not action then
					return
				end
				if action.id ~= "KnifeThrow" and action.id ~= "ThrowKnife" then
					return
				end
				if attacker:GetEffectValue("Jazz_GraceKnifeUsed") then
					return
				end
				if not IsKindOf(attack_target, "Unit") then
					return
				end
				local dist = DivRound(attacker:GetDist(attack_target), const.SlabSizeX)
				if dist <= 12 then
					ApplyCthModifier_Add(self, data, 100)
					data.min = 100
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not action then
					return
				end
				if action.id == "KnifeThrow" or action.id == "ThrowKnife" then
					attacker:SetEffectValue("Jazz_GraceKnifeUsed", true)
				end
			end,
		}),
	},
	DisplayName = T(890000000005039, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Grace DisplayName]] "Точный бросок"),
	Description = T(890000000005040, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Grace Description]] "Первый бросок ножа за ход автоматически попадает по цели в ≤12 клеток."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Grace.png",
	Tier = "Personal",
}
