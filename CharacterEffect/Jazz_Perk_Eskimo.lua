UndefineClass('Jazz_Perk_Eskimo')
DefineClass.Jazz_Perk_Eskimo = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if target ~= attacker or id ~= "Wounded" then
					return
				end
				if IsKindOf(weapon1, "Firearm") then
					data.mod_add = 0
					data.mod_mul = 100
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnStatusEffectAdded",
			Handler = function (self, target, id, stacks)
				if id ~= "Panicked" then
					return
				end
				local hp = (target.HitPoints or 0) + (target.TempHitPoints or 0)
				local maxhp = target.MaxHitPoints or hp or 1
				if maxhp > 0 and MulDivRound(hp, 100, maxhp) < 50 then
					target:RemoveStatusEffect("Panicked")
				end
			end,
		}),
	},
	DisplayName = T(890000000005027, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Eskimo DisplayName]] "Тюремная выдержка"),
	Description = T(890000000005028, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Eskimo Description]] "Ниже 50% HP не получает Панику; раны не режут его CTH из винтовки."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Eskimo.png",
	Tier = "Personal",
}
