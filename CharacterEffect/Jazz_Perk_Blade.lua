UndefineClass('Jazz_Perk_Blade')
DefineClass.Jazz_Perk_Blade = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results or results.miss then
					return
				end
				if not action or action.id ~= "Brutalize" then
					return
				end
				if not IsKindOf(attack_target, "Unit") or attack_target:IsDead() then
					return
				end
				-- Extra hit: deal another Brutalize-scale damage package once per successful strike.
				if attacker:GetEffectValue("Jazz_BladeExtraBusy") then
					return
				end
				attacker:SetEffectValue("Jazz_BladeExtraBusy", true)
				local dmg = results.total_damage or results.damage or 0
				if dmg <= 0 and results.hit_objs then
					for _, hit in ipairs(results.hit_objs) do
						if hit == attack_target or (IsKindOf(hit, "table") and hit.obj == attack_target) then
							dmg = hit.damage or dmg
						end
					end
				end
				if dmg > 0 and attack_target.TakeDirectDamage then
					attack_target:TakeDirectDamage(dmg, false, "Brutalize", attacker)
				elseif dmg > 0 and attack_target.TakeDamage then
					attack_target:TakeDamage(dmg, attacker)
				end
				attacker:SetEffectValue("Jazz_BladeExtraBusy", nil)
			end,
		}),
	},
	DisplayName = T(890000000001800, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Blade DisplayName]] "Вырезать алфавит"),
	Description = T(890000000001801, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Blade Description]] "Зверство: за каждый успешный удар в цепочке наносится ещё один удар."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Blade.png",
	Tier = "Personal",
}
