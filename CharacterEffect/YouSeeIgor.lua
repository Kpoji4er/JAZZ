UndefineClass('YouSeeIgor')
DefineClass.YouSeeIgor = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results then
					return
				end
				local killed = false
				if results.killed_units then
					for _, u in ipairs(results.killed_units) do
						if IsValid(u) then
							killed = true
							break
						end
					end
				end
				if not killed and IsKindOf(attack_target, "Unit") and attack_target:IsDead() then
					killed = true
				end
				if not killed then
					return
				end
				attacker:GainAP(3 * const.Scale.AP)
			end,
		}),
	},
	DisplayName = T(890000000006500, --[[ModItemCharacterEffectCompositeDef YouSeeIgor DisplayName]] "Видишь, Игорь…"),
	Description = T(890000000006501, --[[ModItemCharacterEffectCompositeDef YouSeeIgor Description]] "За каждое убийство получает <em>+3 ОД</em> (не полное восстановление ОД)."),
	Icon = "UI/Icons/Perks/YouSeeIgor",
	Tier = "Personal",
}
