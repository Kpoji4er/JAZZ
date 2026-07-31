UndefineClass('Jazz_Perk_Dynamo')
DefineClass.Jazz_Perk_Dynamo = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcDamageAndEffects",
			Handler = function (self, owner, attacker, target, action, weapon, attack_args, hit, data)
				if owner ~= attacker or not hit or hit.stray then
					return
				end
				if not IsKindOf(target, "Unit") or not attacker:IsOnEnemySide(target) then
					return
				end
				local spot = hit.spot_group or hit.target_spot_group or (attack_args and attack_args.target_spot_group)
				if spot == "Head" and InteractionRand(100, "Jazz_Perk_Dynamo") < 25 then
					target:AddStatusEffect("Blinded")
				end
			end,
		}),
	},
	DisplayName = T(890000000003400, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Dynamo DisplayName]] "Вилкой в глаз"),
	Description = T(890000000003401, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Dynamo Description]] "Попадание в голову: 25% шанс ослепить цель на 1 ход."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Dynamo.png",
	Tier = "Personal",
}
