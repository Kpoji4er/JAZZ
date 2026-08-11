UndefineClass('KillingWind')
DefineClass.KillingWind = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "gritPerEnemyHit",
			'Value', 8,
			'Tag', "<gritPerEnemyHit>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker then return end

				local enemiesHit = 0
				if results and results.hit_objs then
					for _, obj in ipairs(results.hit_objs) do
						if IsKindOf(obj, "Unit") and obj:IsOnEnemySide(attacker) then
							enemiesHit = enemiesHit + 1
						end
					end
				end

				if enemiesHit >= 2 then
					local grit = self:ResolveValue("gritPerEnemyHit") * enemiesHit
					attacker:ApplyTempHitPoints(grit)
				end
			end,
		}),
	},
	DisplayName = T(890000000009875, --[[ModItemCharacterEffectCompositeDef KillingWind DisplayName]] "Убийственный ветер"),
	Description = T(890000000009876, --[[ModItemCharacterEffectCompositeDef KillingWind Description]] "При попадании по ≥2 врагам: +<gritPerEnemyHit> Grit за каждого. Штраф Free Move от тяжёлой брони −50%; громоздкое оружие не лишает Free Move."),
	Icon = "UI/Icons/Perks/KillingWind",
	Tier = "Personal",
}
